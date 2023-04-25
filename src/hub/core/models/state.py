from django.db import models

from base import BaseModel


class State(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")
    owner = models.ForeignKey("Role", blank=True, null=True,
                              on_delete=models.CASCADE, related_name="states")
    info = models.TextField(default="", blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.name
