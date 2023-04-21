from django.db import models

from base import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=250, default="")

    def __str__(self) -> str:
        return self.name
