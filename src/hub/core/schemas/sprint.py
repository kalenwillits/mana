from datetime import date

from base import BaseSchema
from .task import PullTaskOut


class PullSprintOut(BaseSchema):
    name: str
    owner__name: str = None
    state__name: str = None
    tasks: list[PullTaskOut] = None
    info: str = None
    start_date: date = None
    end_date: date = None
