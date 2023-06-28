# Standard Library
import uuid as uuid

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Project
from accounts.consts import STATUS_CHOICES


class UUIDMixin(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name='ID')

    class Meta:
        abstract = True


class Users(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name='ID')
    birth_date = models.DateField(blank=True, null=True)

    class Meta:  # noqa: D106
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):  # noqa: D105
        return f'{self.first_name} {self.last_name} '


class Friendship(UUIDMixin, models.Model):
    from_user = models.ForeignKey(Users, related_name='sender', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Users, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=1)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):  # noqa: D105
        return f'{self.from_user} {self.to_user} '
