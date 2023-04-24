from django.db import models

from base import PrivateModel
from base import fields


class Sprint(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    name = fields.PublicCharField(max_length=250, default="")
    owner = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE,
                                    related_name="sprint_owner")
    info = fields.PublicTextField(default="", blank=True, null=True)
    project = fields.PublicForeignKey("Project", on_delete=models.CASCADE, related_name="sprints")
    state = fields.PublicForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="sprint_states")
    start_date = fields.PublicDateField(blank=True, null=True)
    end_date = fields.PublicDateField(blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}"
