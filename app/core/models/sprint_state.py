from base import PrivateModel
from base import fields


class SprintState(PrivateModel):
    name = fields.PublicCharField(max_length=250, default="")
    description = fields.PublicTextField(default="", blank=True, null=True)
