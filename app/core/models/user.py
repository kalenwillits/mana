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
    tags = fields.PublicManyToManyField("Tag", blank=True)

    objects = BaseUserManager()
