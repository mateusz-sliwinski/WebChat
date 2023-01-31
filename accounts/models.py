import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:  # noqa: D106
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):  # noqa: D105
        return f'{self.first_name} {self.last_name}'
