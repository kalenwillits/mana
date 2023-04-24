from django.db.models import TextField

from base.access import Public
from base.access import Private


class PublicTextField(Public, TextField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateTextField(Private, TextField):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)
