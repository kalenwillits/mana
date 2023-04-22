from base import PrivateModel
from base import fields


class ProjectState(PrivateModel):
    name = fields.PublicCharField(max_length=250)
    description = fields.PublicTextField(default="", blank=True, null=True)

    def __str__(self) -> str:
        return self.name
