from datetime import datetime
from base import BaseSchema


class PullCommentOut(BaseSchema):
    created_at: datetime
    user__username: str
    text: str
