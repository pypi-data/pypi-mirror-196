import os
import json
import sys
import time
import tqdm
from redis import Redis
from chans import config
from chans import chans
from chans import util
from chans.chans.base import Chan


class Scraper:

    def __init__(
        self,
        chans: tuple[Chan, ...] = (chans.Ch2, chans.Ch4),
    ):
        self._chans: list[Chan] = chans
        self.redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)

    def chan_boards_key(self, chan: Chan) -> str:
        return f'{config.PREFIX}:boards:{chan.name}'

    def clean(self):
        util.delete_keys(f'{config.PREFIX}:', self.redis)

    def boards(self):
        pipeline = self.redis.pipeline()
        for chan in self._chans:
            key = self.chan_boards_key(chan)
            pipeline.delete(key)
            pipeline.sadd(key, *chan.boards())
        pipeline.execute()

    def posts(self):
        t = tqdm.tqdm(self._chans)
        for chan in self._chans:
            boards = self.redis.smembers(self.chan_boards_key(chan))
            for board in tqdm.tqdm(boards, leave=False):
                for post_raw in tqdm.tqdm(chan.board_posts_raw(board), leave=False):
                    post = chan.preprocess_post(post_raw)
                    if post.n_replies < config.MIN_REPLIES:
                        t.set_description(f'{chan.name} {board} {post.id} {post.comment[:100]} TOO FEW REPLIES')
                        continue
                    lifetime = time.time() - post.timestamp
                    if lifetime > config.EXPIRE_SECONDS:
                        t.set_description(f'{chan.name} {board} {post.id} {post.comment[:100]} EXPIRED')
                        continue
                    t.set_description(f'{chan.name} {board} {post.id} {post.comment[:100]} SAVE')

                    thread_posts_raw = chan.thread_posts_raw(board, post.id)

                    ttl = int(config.EXPIRE_SECONDS - lifetime)
                    key_raw = f'{config.PREFIX}:posts_raw:{chan.name}:{board}:{post.id}'
                    key_thread_posts_raw = f'{config.PREFIX}:thread_posts_raw:{chan.name}:{board}:{post.id}'
                    key = f'{config.PREFIX}:posts:{chan.name}:{board}:{post.id}'
                    pipeline = self.redis.pipeline()
                    pipeline.set(key_raw, json.dumps(post_raw, ensure_ascii=False))
                    pipeline.set(key_thread_posts_raw, json.dumps(thread_posts_raw, ensure_ascii=False))
                    pipeline.hset(key, mapping=post.dict())
                    pipeline.expire(key_raw, ttl)
                    pipeline.expire(key_thread_posts_raw, ttl)
                    pipeline.expire(key, ttl)
                    pipeline.execute()


    def __call__(self):
        pass


def parse():
    scraper = Scraper()
    scraper.boards()
    scraper.posts()

if __name__ == '__main__':
    # scraper = Scraper(chans=(chans.Ch4,))
    if len(sys.argv) == 2 and sys.argv[1] == 'clean':
        Scraper().clean()
        raise SystemExit
    parse()
