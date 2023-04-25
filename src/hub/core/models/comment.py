from django.db import models

from base import BaseModel


class Comment(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default="")
    tags = models.ManyToManyField("Tag", blank=True)
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    sprint = models.ForeignKey("Sprint", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey("Task", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
