from django.db import models

from base import PrivateModel
from base import fields


class Project(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    author = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    name = fields.PublicCharField(max_length=250, default="")
    threads = fields.PublicManyToManyField("Thread", blank=True)
    state = fields.PublicForeignKey("ProjectState", blank=True, null=True, on_delete=models.SET_NULL)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return f"{self.name}{self.state.name if self.state else None}"
