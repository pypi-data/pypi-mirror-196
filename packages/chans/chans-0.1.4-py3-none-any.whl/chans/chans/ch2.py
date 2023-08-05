import collections
import re
from chans import util
from chans.schemas import Post
from chans.schemas import ViralReply
from typing import Any

from chans.chans.base import Chan
from chans import util


class Ch2(Chan):
    name = '2ch'
    host = 'https://2ch.hk'
    post_id_field = 'num'
    comment_field = 'comment'

    @classmethod
    def boards(cls) -> list[str]:
        return [board['id'] for board in util.retry_request(f'{cls.host}/index.json').json()['boards']]

    @classmethod
    def board_posts_raw(cls, board: str) -> list[dict]:
        return util.retry_request(f'{cls.host}/{board}/catalog.json').json()['threads']
    
    @classmethod
    def preprocess_post(cls, post: dict[str, Any]) -> Post:
        id_ = post[cls.post_id_field]
        post['id'] = id_
        post['url'] = f"{cls.host}/{post['board']}/res/{id_}.html"
        post['comment'] = cls.extract_comment(post, candidate_fields=['subject', 'comment'])
        post['chan'] = cls.name
        post['n_replies'] = post['posts_count']
        return Post(**post)

    @classmethod
    def thread_posts_raw(cls, board: str, thread_id: int) -> list[dict]:
        return util.retry_request(f"{cls.host}/{board}/res/{thread_id}.json").json()['threads'][0]['posts']
    
    def extract_replies(post_raw: dict) -> set[int]:
        return {int(x) for x in re.findall(r'(?<=#)\d+(?=" class="post-reply-link")', post_raw['comment'])}

    # @classmethod
    # def viral_replies(cls, post: Post, top_k: int = 3, min_replies: int = 5) -> list[Post]:
    #     T = cls.thread_posts_raw(post.board, post.id)
    #     # if not T:
    #         # return []
    #     T = T[1:] # delete OP post
        
    #     quotes = collections.Counter()

    #     for t in T:
    #         com = t['comment']
    #         q = map(int, set(re.findall(r'(?<=#)\d+(?=" class="post-reply-link")', com)))
    #         quotes.update(q)

    #     t0 = T[0]['num']
    #     most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
    #     if t0 in most_quoted: # delete OP post
    #         del most_quoted[t0]

    #     for t in T:
    #         if count := most_quoted.get(t['num']):
    #             yield util.html2text(t['comment'], newline=False), count
