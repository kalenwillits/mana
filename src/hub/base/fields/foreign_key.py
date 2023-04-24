from django.db.models import ForeignKey

from base.access import Public
from base.access import Private


class PublicForeignKey(Public, ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateForeignKey(Private, ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)
