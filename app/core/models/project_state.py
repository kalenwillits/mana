from django.db import models

from base import BaseModel


class ProjectState(BaseModel):
    name = models.CharField(max_length=250, default="")
    description = models.TextField(default="")

    def __str__(self) -> str:
        return self.name
