from django.shortcuts import render
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from .consumers import ChatConsumer

class ChatAPIView(APIView):
    def get(self, request, room_name, format=None):
        # Pobierz warstwę kanałów
        channel_layer = get_channel_layer()

        # Utwórz konsumenta czatu
        chat_consumer = ChatConsumer()

        # Połącz konsumenta z pokojem
        async_to_sync(channel_layer.group_add)(
            'chat_%s' % room_name,
            chat_consumer.channel_name
        )

        # Przetwarzaj żądania WebSocket
        chat_consumer.scope = self.request.scope
        chat_consumer.connection = self.request.connection
        chat_consumer.handle()

        return Response(status=200)

class MessageAPIView(APIView):
    def post(self, request, format=None):
        room_name = request.data.get('room_name')
        message_text = request.data.get('message')

        # Tworzenie nowej wiadomości
        message = Message(room_name=room_name, text=message_text)
        message.save()

        # Wysyłanie wiadomości do grupy pokoju za pomocą warstwy kanałów
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % room_name,
            {
                'type': 'chat_message',
                'message': message_text
            }
        )

        return Response(status=201)