# Standard Library
import uuid as uuid

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from accounts.consts import STATUS_CHOICES


# Create your models here.
class Users(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:  # noqa: D106
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):  # noqa: D105
        return f'{self.first_name} {self.last_name} '


class Friendship(models.Model):
    from_user = models.ForeignKey(Users, related_name='sender', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Users, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,default=1)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):  # noqa: D105
        return f'{self.from_user} {self.to_user} '
