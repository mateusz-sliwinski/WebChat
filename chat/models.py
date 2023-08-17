# Django
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Users

User = get_user_model()


# Create your models here.

# class Contact(models.Model):
#     user = models.ForeignKey(Users, related_name='friends', on_delete=models.CASCADE)
#     friends = models.ManyToManyField('self', blank=True)
#
#     def __str__(self):
#         return f'{self.user.username}'

class Participant(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', related_name='participants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} in {self.chat}'


class ChatMessage(models.Model):
    participant = models.ForeignKey(Participant, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.participant.user.username}: {self.content}'


class Chat(models.Model):
    def __str__(self):
        return f'Chat {self.pk}'

    def last_10_messages(self):
        return self.messages.order_by('-timestamp')[:10]

# class Message(models.Model):
#     contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField(max_length=1000)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.contact.user.username} {self.content}'

# class Chat(models.Model):
#     participants = models.ManyToManyField(Contact, related_name='chats')
#     messages = models.ManyToManyField(Message, blank=True)
#
#     def last_10_messages(self):
#         return self.messages.order_by('-timestamp')[:10]
#
#     def __str__(self):
#         return f'{self.pk}'
