from datetime import date

from base import BaseSchema

from .comment import PullCommentOut


class UseSprintIn(BaseSchema):
    name: str


class NewSprintIn(BaseSchema):
    name: str
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = []


class PushSprintIn(BaseSchema):
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = None


class SetSprintIn(BaseSchema):
    state: str


class DropSprintIn(BaseSchema):
    name: str


class PullSprintOut(BaseSchema):
    name: str
    owner__name: str = None
    state__name: str = None
    info: str = None
    start_date: date = None
    end_date: date = None
    comments: list[PullCommentOut] = None
