from django.db import models

from base import PrivateModel
from base import fields


class Task(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    author = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="+")
    name = fields.PublicCharField(max_length=250, default="")
    asignee = fields.PublicForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    sprint = fields.PublicForeignKey("Sprint", on_delete=models.CASCADE, related_name="tasks")
    state = fields.PublicForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="task_states")
    estimate = fields.PublicIntegerField(default=0)
    priority = fields.PublicIntegerField(default=0)
    start_date = fields.PublicDateField(blank=True, null=True)
    end_date = fields.PublicDateField(blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}"
