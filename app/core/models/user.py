from django.db import models
from django.contrib.auth.models import AbstractUser

from base import PrivateModel
from base import BaseUserManager


class User(AbstractUser, PrivateModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    groups = None
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, related_name="role", null=True, blank=True)
    tags = models.ManyToManyField("Tag")

    objects = BaseUserManager()
