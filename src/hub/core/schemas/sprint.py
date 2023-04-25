from base import BaseSchema

from .task import PullTaskOut


class PullSprintOut(BaseSchema):
    name: str
    owner__username: str = None
    tasks: list[PullTaskOut]
    info: str = None
