from django.db.models import CharField

from base.access import Public
from base.access import Private


class PublicCharField(Public, CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateCharField(Private, CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)
