# Django
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Users
from accounts.models import UUIDMixin

User = get_user_model()


class Participant(UUIDMixin, models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', related_name='participants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} in {self.chat}'


class ChatMessage(UUIDMixin, models.Model):
    participant = models.ForeignKey(Participant, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.participant.user.username}: {self.content}'


class Chat(UUIDMixin, models.Model):
    def __str__(self):
        return f'Chat {self.pk}'
