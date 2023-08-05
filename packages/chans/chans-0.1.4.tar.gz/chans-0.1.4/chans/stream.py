import time
import random
import difflib
import pipe21 as P
from chans import util
from chans.util import color_string
from chans.util import color_i
from chans import chans
from chans.chans.base import Chan
from chans import util
from chans import schemas


def sleep_time(posts_count) -> float:
    return -12 * 0.7 ** (0.03 * posts_count) + 12


def prepare_posts(posts: list[schemas.Post]):
    random.shuffle(posts)

    for post in posts:
        t0 = time.time()
        # thread['title_color'] = util.color(thread['posts_count'])
        lifetime_seconds = time.time() - post.timestamp
        derivative = int(post.n_replies / lifetime_seconds * 1000)

        print(post)
        viral_replies = []
        cls: Chan = {'4ch': chans.Ch4, '2ch': chans.Ch2}[post.chan]
        for comment, n_replies in cls.viral_replies(post, top_k=3, min_replies=5):
            viral_replies.append(schemas.ViralReply(comment=comment, n_replies=n_replies))

        yield schemas.StreamPost(
            **post.dict(),
            derivative=derivative,
            sleep_time=max(sleep_time(post.n_replies) - (time.time() - t0), 0),
            viral_replies=viral_replies,
        )
