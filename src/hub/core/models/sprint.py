from django.db import models

from base import BaseModel


class Sprint(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")
    owner = models.ForeignKey("Role", blank=True, null=True,  on_delete=models.CASCADE,
                              related_name="sprints")
    info = models.TextField(default="", blank=True, null=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="sprints")
    state = models.ForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="sprints")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def is_draft(self) -> bool:
        if not self.state:
            return True
        return False

    def __str__(self) -> str:
        return f"{self.name}::{self.state.name if self.state else None}{'(draft)' if self.is_draft() else ''}"
