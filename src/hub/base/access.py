from enum import Enum


class Access(Enum):
    PRIVATE = 0
    PUBLIC = 1


class Public:
    _access: int = Access.PUBLIC.value
    _static_kwargs: dict = {}


class Private:
    _access: int = Access.PRIVATE.value
    _static_kwargs: dict = {
        "editable": False,
    }
