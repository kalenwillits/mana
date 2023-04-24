from django.db import models

from base import PrivateModel
from base import fields


class Comment(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    owner = fields.PublicForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = fields.PublicTextField(default="")

    link = fields.PublicForeignKey("Link", on_delete=models.CASCADE)

    tags = fields.PublicManyToManyField("Tag", blank=True)
