from django.db import models

from base import PrivateModel
from base import fields


class Tag(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    name = fields.PublicCharField(max_length=250, default="")

    def __str__(self) -> str:
        return self.name
