from django.db import models

from base import PrivateModel
from base import fields


class Thread(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    author = fields.PublicForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = fields.PublicTextField(default="")
    thread = fields.PublicForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    project = fields.PublicForeignKey("Project", blank=True, null=True, related_name="projects",
                                      on_delete=models.SET_NULL)
    sprint = fields.PublicForeignKey("Sprint", blank=True, null=True, related_name="sprints", on_delete=models.SET_NULL)
    task = fields.PublicForeignKey("Task", blank=True, null=True, related_name="tasks", on_delete=models.SET_NULL)

    tags = fields.PublicManyToManyField("Tag", blank=True)
