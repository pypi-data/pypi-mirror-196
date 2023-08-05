import json
import abc
from typing import Any
from chans.schemas import Post
from chans import util
import collections
from redis import Redis
from chans import config


class Chan(abc.ABC):
    
    post_id_field: str
    comment_field: str

    @classmethod
    @abc.abstractmethod
    def boards(cls) -> list[str]:
        ...

    @classmethod
    @abc.abstractmethod
    def board_posts_raw(cls, board: str) -> list[dict]:
        ...

    @classmethod
    @abc.abstractmethod
    def preprocess_post(cls, post: dict) -> Post:
        ...

    @classmethod
    @abc.abstractmethod
    def thread_posts_raw(cls, board: str, thread_id: int) -> list[dict]:
        ...

    @classmethod
    @abc.abstractmethod
    def extract_replies(reply_raw: dict) -> set[int]:
        ...

    @classmethod
    def viral_replies(
        cls, 
        post: Post, 
        top_k: int = 3, 
        min_replies: int = 5,
        redis: Redis | None = None,
    ) -> list[Post]:
        """
        if redis is not None, it will be used to load thread data instead of making a request to API
        """
        if redis is not None:
            T = redis.get(f'{config.PREFIX}:thread_posts_raw:{cls.name}:{post.board}:{post.id}')
            if T is None:
                return []
            T = json.loads(T)
        T = cls.thread_posts_raw(post.board, post.id)
        # if not T:
            # return []
        assert T is not None, T
        T = T[1:] # delete OP post
        quotes = collections.Counter()
        for t in T:
            q = cls.extract_replies(t)
            quotes.update(q)
        most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
    
        for t in T:
            if count := most_quoted.get(t[cls.post_id_field]):
                yield util.html2text(t[cls.comment_field], newline=False), count

    @classmethod
    def extract_comment(cls, post: dict[str, Any], candidate_fields: list[str]) -> str:
        candidate_fields = set(candidate_fields) & post.keys()
        candidates = {util.html2text(post[field]) for field in candidate_fields if post[field]}
        # todo: use difflib to drop similar comments
        return ' '.join(candidates)
    


  # if comment := thread.get('comment'):
        #     comment = util.html2text(comment, newline=True)
        #     nospace_title = [c for c in thread['title'] if not c.isspace()]
        #     nospace_comment = [c for c in comment if not c.isspace()]
        #     min_len = min(len(nospace_title), len(nospace_comment))
        #     ratio = difflib.SequenceMatcher(lambda x: x.isspace(), nospace_title[:min_len], nospace_comment[:min_len]).ratio()

        #     if ratio < 0.7:
        #         thread['title'] = thread['title']
        #     else:
        #         thread['title'] = comment[:500]
