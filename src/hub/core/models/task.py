from django.db import models

from base import BaseModel


class Task(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    owner = models.ForeignKey("User", blank=True, null=True,  on_delete=models.CASCADE, related_name="task_owner")
    name = models.CharField(max_length=250, default="")
    info = models.TextField(default="", blank=True, null=True)
    asignee = models.ForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL,
                                related_name="task_asignee")
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, related_name="tasks")
    state = models.ForeignKey("State", blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="task_states")
    estimate = models.IntegerField(default=0, blank=True, null=True)
    priority = models.IntegerField(default=0, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        state_name = None
        if self.state:
            state_name = self.state.name

        return f"{self.name}::{state_name}"
