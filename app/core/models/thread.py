from django.db import models

from base import PrivateModel
from base import fields


class Thread(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    author = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    text = fields.PublicTextField(default="")
    threads = fields.PublicManyToManyField("self", blank=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)
