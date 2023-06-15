from django.db import models
from accounts.models import Users

class ChatMessage(models.Model):
    text = models.TextField(max_length=512)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class ChatRoom(models.Model):
    name = models.CharField(max_length=128, default='')
    message_id = models.ForeignKey(ChatMessage, models.CASCADE)


