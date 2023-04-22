from enum import Enum


class Access(Enum):
    PRIVATE = 0
    PUBLIC = 1


class Public:
    _access = Access.PUBLIC.value


class Private:
    _access = Access.PRIVATE.value

