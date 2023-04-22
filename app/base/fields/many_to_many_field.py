from django.db.models import ManyToManyField

from base.access import Public
from base.access import Private


class PublicManyToManyField(Public, ManyToManyField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PrivateManyToManyField(Private, ManyToManyField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
