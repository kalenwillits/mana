from django.db import models
from django.contrib.auth.models import Group

from base import BaseModel


class Role(Group, BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    info = models.TextField(default="", blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    class Meta:
        app_label = "core"
        verbose_name = "Role"

    def __str__(self) -> str:
        return self.name
