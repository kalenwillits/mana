from django.db import models
from django.contrib.auth.models import AbstractUser

from base import PrivateModel
from base import BaseUserManager
from base import fields


class User(AbstractUser, PrivateModel):
    groups = None

    organization = fields.PrivateForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    role = fields.PrivateForeignKey("Role", on_delete=models.SET_NULL, related_name="role", null=True, blank=True)

    objects = BaseUserManager()
    tags = fields.PublicManyToManyField("Tag", blank=True)

    project = fields.PublicForeignKey("Project", blank=True, null=True, on_delete=models.SET_NULL)
    sprint = fields.PublicForeignKey("Sprint", blank=True, null=True, on_delete=models.SET_NULL)
    task = fields.PublicForeignKey("Task", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        role_name = None
        if self.role:
            role_name = self.role.name
        return f"{self.username}::{role_name}"
