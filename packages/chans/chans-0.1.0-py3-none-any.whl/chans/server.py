from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import WebSocket
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pathlib import Path
import subprocess
import asyncio
from redis.asyncio import Redis
import threading


from chans import chans
from chans import util
from chans import data
from chans import config
from chans import parser
from chans.stream import prepare_posts
from chans.dependencies import get_redis_async


parser_thread = threading.Thread(target=parser.parse)
parser_thread.start()


static_folder = Path(__file__).parent / 'static'
templates = Jinja2Templates(directory=static_folder / 'templates')
templates.env.filters['format_time'] = util.format_time

app = FastAPI()
app.mount('/static/', StaticFiles(directory=static_folder), name='static')


@app.get('/favicon.ico', response_class=HTMLResponse)
async def favicon():
    return FileResponse(static_folder / 'favicon.ico')


@app.get('/', response_class=HTMLResponse)
async def get_chan(
    request: Request,
    min_replies: int = 10,
    redis: Redis = Depends(get_redis_async),
):
    posts = await data.posts(redis, min_replies=min_replies)
    return templates.TemplateResponse(
        'posts.j2', {
            'request': request,
            'posts': posts,
        },
    )


@app.get('/stream', response_class=HTMLResponse)
def stream(request: Request):
    return templates.TemplateResponse(
        'stream.j2', {
            'request': request,
            'port': config.PORT,
        },
    )

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    redis: Redis = Depends(get_redis_async),
):
    posts = await data.posts(redis)
    posts = prepare_posts(posts)
    await websocket.accept()
    for post in posts:
        card_html = templates.get_template('card.j2').render(post=post)
        await websocket.send_text(card_html)
        await asyncio.sleep(post.sleep_time)


@app.get('/settings', response_class=HTMLResponse)
async def settings(
    request: Request,
):
    return templates.TemplateResponse(
        'settings.j2', {
            'request': request,
        },
    )


def main():
    cmd = ["uvicorn", "chans.server:app", "--host", "0.0.0.0", "--port", config.PORT]
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
