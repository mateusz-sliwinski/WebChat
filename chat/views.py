from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from .serializers import ChatSerializer
from .models import Chat, Participant

User = get_user_model()


class ChatView(ListAPIView):
    serializer_class = ChatSerializer
    name = 'room'
    permission_classes = [AllowAny]

    def get_queryset(self):
        from_uuid = self.request.GET.get('from_uuid')
        to_uuid = self.request.GET.get('to_uuid')
        participants_from_user = Participant.objects.filter(user__id=from_uuid)
        participants_to_user = Participant.objects.filter(user__id=to_uuid)
        chat_id = None
        for participant_from in participants_from_user:
            for participant_to in participants_to_user:
                if participant_from.chat == participant_to.chat:
                    chat_id = participant_from.chat.id

        return Chat.objects.filter(id=chat_id)
