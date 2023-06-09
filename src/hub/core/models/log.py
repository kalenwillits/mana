from django.contrib.contenttypes.models import ContentType
from django.db import models

from base import BaseModel
from .link import Link

HEADER_LENGTH: int = 250


class Log(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    info = models.TextField(default="", blank=True, null=True)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    link = models.ForeignKey("Link", blank=True, null=True, on_delete=models.CASCADE)

    def __setattr__(self, attr: str, value: any):
        if attr == "link":
            self._link(value)
        else:
            super().__setattr__(attr, value)

    def _link(self, obj):
        target_type = None
        target_id = None
        target_object = None
        if obj:
            target_type = ContentType.objects.get_for_model(obj)
            target_id = target_type.id
            target_object = obj
        super().__setattr__("link", Link(
            organization=self.organization,
            target_type=target_type,
            target_id=target_id,
            target_object=target_object
        ))

    def save(self):
        if hasattr(self, "link"):
            self.link.save()
        super().save()

    def __str__(self):
        return f"{self.created_at} {self.info[:HEADER_LENGTH]}"
