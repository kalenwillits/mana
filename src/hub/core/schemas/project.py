from datetime import date

from base import BaseSchema
from .tag import TagOut
from .sprint import PullSprintOut


class UseProjectIn(BaseSchema):
    name: str


class NewProjectIn(BaseSchema):
    name: str
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = []


class PushProjectIn(BaseSchema):
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = None


class SetProjectIn(BaseSchema):
    state: str


class DropProjectIn(BaseSchema):
    name: str


class PullProjectOut(BaseSchema):
    name: str
    owner__name: str = None
    state__name: str = None
    sprints: list[PullSprintOut] = None
    info: str
    start_date: date
    end_date: date
    tags: list[TagOut] = None
