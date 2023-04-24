from django.db.models import IntegerField

from base.access import Public
from base.access import Private


class PublicIntegerField(Public, IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateIntegerField(Private, IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)
