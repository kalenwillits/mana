from django.db import models

from base import PrivateModel
from base import fields


class Task(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    owner = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="task_owner")
    name = fields.PublicCharField(max_length=250, default="")
    info = fields.PublicTextField(default="", blank=True, null=True)
    asignee = fields.PublicForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL,
                                      related_name="task_asignee")
    sprint = fields.PublicForeignKey("Sprint", on_delete=models.CASCADE, related_name="tasks")
    state = fields.PublicForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="task_states")
    estimate = fields.PublicIntegerField(default=0, blank=True, null=True)
    priority = fields.PublicIntegerField(default=0, blank=True, null=True)
    start_date = fields.PublicDateField(blank=True, null=True)
    end_date = fields.PublicDateField(blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        state_name = None
        if self.state:
            state_name = self.state.name

        return f"{self.name}::{state_name}"
