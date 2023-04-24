from django.db import models

from base import BaseModel


class State(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")
    info = models.TextField(default="", blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.name
