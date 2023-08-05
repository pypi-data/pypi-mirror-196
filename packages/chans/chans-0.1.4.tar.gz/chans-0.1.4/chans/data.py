import operator
from redis import Redis
from chans.schemas import Post
from chans import config
import pipe21 as P


async def posts(
    redis: Redis,
    chans: frozenset[str] | None = None,
    boards: frozenset[str] | None = None,
    min_replies: int = 0,
    sortby: str = 'n_replies', 
    reverse: bool = True,
) -> list[Post]:
    keys = await redis.keys(f'{config.PREFIX}:posts:*')
    keys_filtered = []
    for key in keys:
        _, _, chan, board, _ = key.split(':')
        if chans is not None and chan not in chans:
            continue
        if boards is not None and board not in boards:
            continue
        keys_filtered.append(key)
    pipeline = redis.pipeline()
    for key in keys_filtered:
        pipeline.hgetall(key)
    posts = await pipeline.execute()
    posts = [Post(**post) for post in posts]
    return (
        posts
        | P.Filter(lambda post: post.n_replies >= min_replies)
        | P.Sorted(key = operator.attrgetter(sortby), reverse=reverse)
        | P.Pipe(list)
    )
