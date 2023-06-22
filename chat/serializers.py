from rest_framework import serializers

from .models import ChatMessage, Chat, Contact


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('__all__')
