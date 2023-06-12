import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Dołącz do grupy pokoju
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Opuść grupę pokoju
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Przetwarzaj otrzymane dane
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Wyślij wiadomość do grupy pokoju
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # Obsługa otrzymanej wiadomości
        message = event['message']

        # Wyślij wiadomość do klienta
        self.send(text_data=json.dumps({
            'message': message
        }))