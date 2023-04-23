from django.db import models

from base import PrivateModel
from base import fields


class Project(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE, related_name="+")
    name = fields.PublicCharField(max_length=250, default="")
    owner = fields.PublicForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE,
                                    related_name="project_owner")

    info = fields.PublicTextField(default="", blank=True, null=True)
    state = fields.PublicForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="project_states")
    start_date = fields.PublicDateField(blank=True, null=True)
    end_date = fields.PublicDateField(blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}"
