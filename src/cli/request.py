import os
import requests


OPERATION_MAP = {
            "use": requests.put,
            "new": requests.post,
            "drop": requests.delete,
            "set": requests.put,
            "push": requests.put,
            "pull": requests.get
        }

OBJECTS = "project", "sprint", "task"


class Request:
    def __init__(self, operation: str, obj: str, arg: str):
        assert operation in OPERATION_MAP.keys(), f"Invalid operation [{operation}]"
        assert obj in OBJECTS, f"Invalid object [{obj}]"
        assert arg, "Missing argument"
        self._base_url = os.environ.get("MANA_HUB_URL", "http://localhost:8000")
        self.operation = operation
        self.obj = obj
        self.arg = arg
        self.username = os.environ.get("MANA_USERNAME")
        self.password = os.environ.get("MANA_PASSWORD")

    def __call__(self) -> requests.Response:
        if method := self.method:
            return method(self.url, headers=self.headers, json=self.body)
        raise ValueError("Invalid arguement")

    @property
    def url(self) -> str:
        return f"{self._base_url}/{self.obj}/{self.operation}/"

    @property
    def headers(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }

    @property
    def body(self) -> dict:
        return {
            "name": self.arg
        }

    @property
    def method(self) -> callable:
        return OPERATION_MAP.get(self.operation)
