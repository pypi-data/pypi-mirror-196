from collections.abc import Callable
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    timestamp: int
    comment: str
    chan: str
    board: str
    n_replies: int
    url: str


# class ViralReply(Post):
class ViralReply(BaseModel):
    comment: str
    n_replies: int


class StreamPost(Post):
    derivative: int
    sleep_time: float
    viral_replies: list[ViralReply]
