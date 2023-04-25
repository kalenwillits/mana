from django.db import models
from django.contrib.contenttypes.models import ContentType


from base import BaseModel
from .link import Link


class Comment(BaseModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(default="")
    link = models.ForeignKey("Link", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    sprint = models.ForeignKey("Sprint", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey("Task", blank=True, null=True, on_delete=models.CASCADE, related_name="comments")

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
