from uuid import uuid4
from datetime import datetime


from django.db import models
from django.contrib.auth.models import UserManager
from django.apps import apps
from ninja import Schema


def use_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


class BaseSchema(Schema):

    @classmethod
    def fields(cls):
        return cls.__fields__.keys()


class BaseManager(models.Manager):
    pass


class BaseUserManager(UserManager, BaseManager):
    pass


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.IntegerField(default=use_timestamp, editable=False)
    updated_at = models.IntegerField(blank=True, null=True, editable=False)

    objects = BaseManager()

    class Meta:
        abstract = True

    def update(self, **kwargs):
        Tag = apps.get_model(app_label="core", model_name="Tag")
        for field, value in kwargs.items():
            if value:
                if field != "tags" and value is not None:
                    setattr(self, field, value)
        if hasattr(self, "tags"):
            tags = kwargs.get("tags", [])
            normalized_tags = list(map(Tag.normalize_str, tags))
            tags_queryset = Tag.objects.filter(organization=self.organization, name__in=normalized_tags)
            new_tags = []
            for tag_name in filter(lambda tag_name: not tags_queryset.filter(name=tag_name).exists(), normalized_tags):
                new_tags.append(Tag(organization=self.organization, name=tag_name))

            Tag.objects.bulk_create(new_tags)
            self.tags.add(*tags_queryset, *new_tags)
        return self

    @staticmethod
    def normalize_str(string: str) -> str:
        return string.strip().replace(" ", "_")

    def __setattr__(self, attr: str, value: any):
        if attr == "name":
            super().__setattr__(attr, self.normalize_str(value))
        else:
            super().__setattr__(attr, value)
