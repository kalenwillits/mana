from datetime import date

from ninja import Schema


class NewProject(Schema):
    name: str
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = []


class PushProject(Schema):
    name: str = None
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = None
