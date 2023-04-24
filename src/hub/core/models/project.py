from django.db import models

from base import BaseModel


class Project(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    name = models.CharField(max_length=250, default="")
    owner = models.ForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE,
                              related_name="project_owner")
    info = models.TextField(default="", blank=True, null=True)
    state = models.ForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="project_states")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}"
