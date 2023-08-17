# chat/consumers.py
# Standard Library
import json

# Django
from django.shortcuts import get_object_or_404

# 3rd-party
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Project
from accounts.models import Users

# Local
from .models import Chat
from .models import ChatMessage
from .models import Participant


def get_user_contact(username, chatId):
    user = get_object_or_404(Users, username=username)
    return get_object_or_404(Participant, user=user, chat=chatId)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        chat_id = data['chatId']
        messages = ChatMessage.objects.all().filter(participant__chat_id=chat_id).order_by('timestamp')
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author_user = get_user_contact(data['username'], data['chatId'])
        message = ChatMessage.objects.create(
            participant=author_user,
            content=data['content'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'participant': message.participant.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))