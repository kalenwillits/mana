from django.db import models

from base import BaseModel


class Task(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    author = models.ForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    name = models.CharField(max_length=250, default="")
    thread = models.ForeignKey("Thread", blank=True, null=True, on_delete=models.CASCADE)
    asignee = models.ForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    sprint = models.ForeignKey("Sprint", blank=True, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("TaskState", blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField("Tag")

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}"
