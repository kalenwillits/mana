from django.db import models
from django.contrib.auth.models import AbstractUser

from base import BaseModel
from base import BaseUserManager


class User(AbstractUser, BaseModel):
    groups = None

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, related_name="role", null=True, blank=True)

    objects = BaseUserManager()
    tags = models.ManyToManyField("Tag", blank=True)

    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.SET_NULL)
    sprint = models.ForeignKey("Sprint", blank=True, null=True, on_delete=models.SET_NULL)
    task = models.ForeignKey("Task", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        role_name = None
        if self.role:
            role_name = self.role.name
        return f"{self.username}::{role_name}"
