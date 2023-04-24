from django.db import models

from base import PrivateModel
from base import fields

HEADER_LENGTH: int = 250


class Log(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    level = fields.PrivateIntegerField(default=0)
    info = fields.PrivateTextField(default="", blank=True, null=True)
    owner = fields.PrivateForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    link = fields.PrivateForeignKey("Link", on_delete=models.CASCADE)

    def __str__(self):
        return self.info[:HEADER_LENGTH]
