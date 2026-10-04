import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )
    class Meta:
        abstract = True


