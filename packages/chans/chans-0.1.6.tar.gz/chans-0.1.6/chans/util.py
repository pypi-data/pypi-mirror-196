import datetime
import itertools
import re
import html
import time
import humanize
from redis import Redis
from typing import Any
import requests
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from tenacity import TryAgain

from chans.dependencies import get_redis_cm
from chans import chans
from chans import config


def delete_keys(prefix: str, redis):
    pipeline = redis.pipeline()
    for key in redis.keys(prefix + '*'):
        pipeline.delete(key)
    _ = pipeline.execute()


def setitem(key, value):
    def inner(x):
        x[key] = value
    return inner



def log_error_to_redis(retry_state):
    error_data, = retry_state.outcome._exception.args
    timestamp = round(time.time() * 1000)
    print(timestamp, error_data)
    with get_redis_cm() as redis:
        redis.hset(f'{config.ERRORS}:{timestamp}', mapping=error_data)


@retry(
    wait=wait_fixed(2),
    stop=stop_after_attempt(3),
    retry_error_callback=log_error_to_redis, 
)
def retry_request(url: str) -> dict:
    r = requests.get(url)
    if not r.ok:
        raise TryAgain({
            'url': url,
            'status_code': r.status_code,
            'text': r.text,
        })
    return r


def html2text(htm, newline=False):
    ret = html.unescape(htm)
    ret = ret.translate({8209: ord('-'), 8220: ord('"'), 8221: ord('"'), 160: ord(' '),})
    ret = re.sub(r"\s", " ", ret, flags = re.MULTILINE)
    if newline:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", '\n', ret, flags = re.IGNORECASE)
    else:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", ' ', ret, flags = re.IGNORECASE)
    ret = re.sub('<.*?>', ' ', ret, flags=re.DOTALL)
    ret = re.sub(r"  +", " ", ret)
    return ret


def color(v):
    if   v <   5: c = 236
    elif v <  10: c = 237
    elif v <  15: c = 238
    elif v <  20: c = 239
    elif v <  25: c = 240
    elif v <  30: c = 241
    elif v <  35: c = 242
    elif v <  40: c = 243
    elif v <  45: c = 244
    elif v <  50: c = 245
    elif v <  55: c = 246
    elif v <  60: c = 247
    elif v <  65: c = 248
    elif v <  70: c = 249
    elif v <  75: c = 250
    elif v <  80: c = 251
    elif v <  85: c = 252
    elif v <  90: c = 253
    elif v <  95: c = 254
    elif v < 100: c = 255
    elif v < 200: c = 82  # green
    elif v < 300: c = 87  # blue
    elif v < 400: c = 226 # yellow
    elif v < 500: c = 208 # orange
    elif v>= 500: c = 196 # red
    return c

class color_string:
    BLACK     = lambda s: '\033[30m' + str(s) + '\033[0m'
    RED       = lambda s: '\033[31m' + str(s) + '\033[0m'
    GREEN     = lambda s: '\033[32m' + str(s) + '\033[0m'
    YELLOW    = lambda s: '\033[33m' + str(s) + '\033[0m'
    BLUE      = lambda s: '\033[34m' + str(s) + '\033[0m'
    MAGENTA   = lambda s: '\033[35m' + str(s) + '\033[0m'
    CYAN      = lambda s: '\033[36m' + str(s) + '\033[0m'
    WHITE     = lambda s: '\033[37m' + str(s) + '\033[0m'
    UNDERLINE = lambda s: '\033[4m'  + str(s) + '\033[0m'


def color_i(s, i):
    return f"\x1b[38;5;{i}m{s}\033[0m"


def to_local_time(dt: datetime.datetime, timezone: datetime.timezone):
    if dt.tzinfo is not None:
        raise ValueError('pass timezone as separate argument')
    dt = dt.replace(tzinfo=timezone)
    return datetime.datetime.fromtimestamp(dt.timestamp())


def format_time(
    t: datetime.datetime | int,
    absolute: bool = False,
    pad: bool = False,
    timezone: datetime.timezone | None = None,
) -> str:
    if isinstance(t, int):
        t = datetime.datetime.fromtimestamp(t)
    if timezone is not None:
        t = to_local_time(t, timezone)
    if absolute or (datetime.datetime.utcnow() - t).days > 30:  # noqa: PLR2004
        return t.strftime('%Y %b %d %H:%M')
    t = datetime.datetime.fromtimestamp(t.timestamp())
    out = humanize.naturaltime(t)
    if pad:
        out = out.rjust(17)
    return out
