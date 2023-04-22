from django.db import models

from base import BaseModel


class Thread(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    author = models.ForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    text = models.TextField(default="")
    thread = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="+")
    tags = models.ManyToManyField("Tag")
