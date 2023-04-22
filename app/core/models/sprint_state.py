from django.db import models

from base import BaseModel


class SprintState(BaseModel):
    name = models.CharField(max_length=250, default="")
    description = models.TextField(default="", blank=True, null=True)
