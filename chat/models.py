# Django
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Users

User = get_user_model()


# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(Users, related_name='author_message', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}'

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]
