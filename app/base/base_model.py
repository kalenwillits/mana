from uuid import uuid4

from datetime import datetime

from django.db import models


def use_timestamp() -> int:
    return int(datetime.now().timestamp())


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.IntegerField(default=use_timestamp, editable=False)
    updated_at = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True
