from django.db import models
from django.contrib.contenttypes.models import ContentType

from base import PrivateModel
from base import fields


class Link(PrivateModel):
    organization = fields.PrivateForeignKey("Organization", on_delete=models.CASCADE)
    target_type = fields.PublicForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = fields.PublicUUIDField()
    target_object = fields.PublicGenericForeignKey("target_type", "target_id")
