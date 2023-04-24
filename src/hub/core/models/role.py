from django.db import models
from django.contrib.auth.models import Group

from base import Private
from base import fields


class Role(Private, Group):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    info = fields.PublicTextField(default="", blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    class Meta:
        app_label = "core"
        verbose_name = "Role"

    def __str__(self) -> str:
        return self.name
