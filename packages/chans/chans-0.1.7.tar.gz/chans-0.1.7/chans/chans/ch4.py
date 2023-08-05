import collections
import re
from chans import util
from chans.chans.base import Chan
from chans.schemas import Post
from typing import Any

import pipe21 as P

class Ch4(Chan):
    name = '4ch'
    host = 'https://4chan.org'
    post_id_field = 'no'
    comment_field = 'com'

    @classmethod
    def boards(cls) -> list[str]:
        return [board['board'] for board in util.retry_request('https://a.4cdn.org/boards.json').json()['boards']]

    @classmethod
    def board_posts_raw(cls, board: str) -> list[dict]:
        return (
            util.retry_request(f'https://a.4cdn.org/{board}/catalog.json').json()
            | P.FlatMap(lambda x: x['threads'])
            | P.ApplyMap(util.setitem('board', board))
            | P.Pipe(list)
        )
    
    @classmethod
    def preprocess_post(cls, post: dict[str, Any]) -> Post:
        id_ = post[cls.post_id_field]
        post['id'] = id_
        post['timestamp'] = post['time']
        post['url'] = f"https://boards.4chan.org/{post['board']}/thread/{id_}"
        post['comment'] = cls.extract_comment(post, candidate_fields=['sub', 'com', 'comment'])
        post['chan'] = cls.name
        post['n_replies'] = post['replies']
        return Post(**post)
    
    @classmethod
    def thread_posts_raw(cls, board: str, thread_id: int) -> list[dict]:
        return util.retry_request(f"https://a.4cdn.org/{board}/thread/{thread_id}.json").json()['posts']

    def extract_replies(post_raw: dict) -> set[int]:
        if com := post_raw.get('com'):
            return {int(x) for x in re.findall(r'(?<=href="#p)\d+(?=" class="quotelink")', com)}
        return set()

    # @classmethod
    # def viral_replies(cls, post: Post, top_k: int = 3, min_replies: int = 5) -> list[Post]:
    #     T = cls.thread_posts_raw(post.board, post.id)
    #     # if not T:
    #         # return []
    #     T = T[1:] # delete OP post

    #     quotes = collections.Counter()

    #     for t in T:
    #         if com := t.get('com'):
    #             q = map(int, set(re.findall(r'(?<=href="#p)\d+(?=" class="quotelink")', com)))
    #             quotes.update(q)

    #     t0 = T[0]['no']
    #     most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
    #     if t0 in most_quoted:
    #         del most_quoted[t0]

    #     for t in T:
    #         if (count := most_quoted.get(t['no'])) and (com := t.get('com')):
    #             yield util.html2text(com, newline=False), count
