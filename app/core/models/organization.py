from base import PrivateModel
from base import fields


class Organization(PrivateModel):
    name = fields.PublicCharField(max_length=250, default="")

    def __str__(self) -> str:
        return self.name
