from uuid import uuid4
from datetime import datetime


from django.db import models
from django.contrib.auth.models import UserManager

from base.fields import PublicUUIDField
from base.fields import PrivateIntegerField
from base.access import Public
from base.access import Private


def use_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


class BaseManager(models.Manager):
    def hydrate(self, *args, **kwargs):
        queryset = self.filter(*args, **kwargs)
        values = []
        for obj in queryset:
            obj_values = {}
            for field in obj._meta.fields:
                obj_class = type(obj)
                field_class = type(field)
                if issubclass(field_class, Public) or \
                    issubclass(obj_class, Public) and \
                        not issubclass(field_class, Private):
                    if not field.is_relation:
                        obj_values[field.name] = getattr(obj, field.name)

                for related_obj in type(obj)._meta.related_objects:
                    if issubclass(type(related_obj.remote_field), Public):
                        obj_values[related_obj.name] = related_obj.related_model.objects.hydrate(**{
                            related_obj.remote_field.name: obj
                        })
            values.append(obj_values)
        return values


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


class PublicModel(BaseModel, Public):
    class Meta:
        abstract = True


class PrivateModel(BaseModel, Private):
    class Meta:
        abstract = True
