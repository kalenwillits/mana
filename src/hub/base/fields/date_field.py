from django.db.models import DateField

from base.access import Public
from base.access import Private


class PublicDateField(Public, DateField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateDateField(Private, DateField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)

