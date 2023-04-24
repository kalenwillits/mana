from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from base import BaseModel


class Link(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.UUIDField()
    target_object = GenericForeignKey("target_type", "target_id")
