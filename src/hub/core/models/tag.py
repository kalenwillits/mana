from django.db import models

from base import BaseModel


class Tag(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")

    def __str__(self) -> str:
        return self.name
