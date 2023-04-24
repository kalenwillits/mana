from django.contrib.contenttypes.fields import GenericForeignKey

from base.access import Public
from base.access import Private


class PublicGenericForeignKey(Public, GenericForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update(Public._static_kwargs)
        super().__init__(*args, **kwargs)


class PrivateGenericForeignKey(Private, GenericForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update(Private._static_kwargs)
        super().__init__(*args, **kwargs)

