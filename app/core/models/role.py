from django.db import models

from django.contrib.auth.models import Group


class Role(Group):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+")

    class Meta:
        app_label = "core"
        verbose_name = "Role"

    def __str__(self) -> str:
        return self.name
