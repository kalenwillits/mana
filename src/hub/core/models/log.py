from django.db import models

from base import BaseModel

HEADER_LENGTH: int = 250


class Log(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    info = models.TextField(default="", blank=True, null=True)
    owner = models.ForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    link = models.ForeignKey("Link", on_delete=models.CASCADE)

    def __str__(self):
        return self.info[:HEADER_LENGTH]
