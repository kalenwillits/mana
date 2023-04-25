from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from base import BaseModel


class Link(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    target_id = models.UUIDField(blank=True, null=True)
    target_object = GenericForeignKey("target_type", "target_id")

    def __str__(self):
        return f"{self.target_type}::{self.target_object}"
