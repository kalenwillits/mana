from datetime import date

from ninja import Schema


class UseProject(Schema):
    name: str


class NewProject(Schema):
    name: str
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = []


class PushProject(Schema):
    info: str = None
    start_date: date = None
    end_date: date = None
    state: str = None
    tags: list[str] = None


class SetProject(Schema):
    state: str


class DropProject(Schema):
    name: str
