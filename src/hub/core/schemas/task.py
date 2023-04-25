from datetime import date
from base import BaseSchema


class PullTaskOut(BaseSchema):
    name: str
    owner__username: str = None
    info: str = None
    estimate: float
    start_date: date
    end_date: date
