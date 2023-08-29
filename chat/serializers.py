# 3rd-party
from rest_framework import serializers

# Project
from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('__all__')
