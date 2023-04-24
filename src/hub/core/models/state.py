from django.db import models

from base import PrivateModel
from base import fields


class State(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    name = fields.PublicCharField(max_length=250, default="")
    info = fields.PublicTextField(default="", blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.name
