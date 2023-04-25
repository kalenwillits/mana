from django.db import models

from base import BaseModel
from .link import Link


class Comment(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default="")
    link = models.ForeignKey("Link", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)

    def __setattr__(self, attr: str, value: any):
        if attr == "link":
            self._link(value)
        else:
            super().__setattr__(attr, value)

    def _link(self, obj):
        super().__setattr__("link", Link(
            organization=self.organization,
            target_type=type(obj),
            target_id=obj.id,
            target_object=obj
        ))

    def save(self):
        if hasattr(self, "link"):
            self.link.save()
        super().save()
