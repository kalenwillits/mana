from datetime import date

from base import BaseSchema

from .comment import PullCommentOut


class UseTaskIn(BaseSchema):
    name: str


class NewTaskIn(BaseSchema):
    name: str
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = []


class PushTaskIn(BaseSchema):
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = None


class SetTaskIn(BaseSchema):
    state: str


class DropTaskIn(BaseSchema):
    name: str


class PullTaskOut(BaseSchema):
    name: str
    sprint__project__name: str
    sprint__name: str
    owner__name: str = None
    state__name: str = None
    info: str = None
    estimate: float = None
    start_date: date = None
    end_date: date = None
    comments: list[PullCommentOut] = None
