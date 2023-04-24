from uuid import uuid4
from datetime import datetime


from django.db import models
from django.contrib.auth.models import UserManager
from django.apps import apps

from base.fields import PublicUUIDField
from base.fields import PrivateIntegerField
from base.access import Public
from base.access import Private


def use_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


class BaseManager(models.Manager):
    pass
    # def hydrate(self, *args, **kwargs):
    #     queryset = self.filter(*args, **kwargs)
    #     values = []
    #     for obj in queryset:
    #         obj_values = {}
    #         for field in obj._meta.fields:
    #             obj_class = type(obj)
    #             field_class = type(field)
    #             if issubclass(field_class, Public) or \
    #                 issubclass(obj_class, Public) and \
    #                     not issubclass(field_class, Private):
    #                 if not field.is_relation:
    #                     obj_values[field.name] = getattr(obj, field.name)

    #             for related_obj in type(obj)._meta.related_objects:
    #                 if issubclass(type(related_obj.remote_field), Public):
    #                     obj_values[related_obj.name] = related_obj.related_model.objects.hydrate(**{
    #                         related_obj.remote_field.name: obj
    #                     })
    #         values.append(obj_values)
    #     return values


class BaseUserManager(UserManager, BaseManager):
    pass


class BaseModel(models.Model):
    id = PublicUUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = PrivateIntegerField(default=use_timestamp, editable=False)
    updated_at = PrivateIntegerField(blank=True, null=True, editable=False)

    objects = BaseManager()

    class Meta:
        abstract = True

    def values(self) -> dict:
        return type(self).objects.filter(pk=self.pk).values().first()

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


class PublicModel(BaseModel, Public):
    class Meta:
        abstract = True


class PrivateModel(BaseModel, Private):
    class Meta:
        abstract = True
