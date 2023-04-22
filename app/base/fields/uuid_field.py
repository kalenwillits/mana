from django.db.models import UUIDField

from base.access import Public
from base.access import Private


class PublicUUIDField(Public, UUIDField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PrivateUUIDField(Private, UUIDField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
