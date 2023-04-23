from base import PrivateModel
from base import fields


class State(PrivateModel):
    name = fields.PublicCharField(max_length=250, default="")
    info = fields.PublicTextField(default="", blank=True, null=True)
    tags = fields.PublicManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.name
