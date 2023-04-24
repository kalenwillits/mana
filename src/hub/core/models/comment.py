from django.db import models

from base import BaseModel


class Comment(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    owner = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default="")
    link = models.ForeignKey("Link", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
