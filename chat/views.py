# Django
from django.contrib.auth import get_user_model
# 3rd-party
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Local
from .models import Chat
from .models import Participant
from .serializers import ChatSerializer

User = get_user_model()


class ChatView(ListAPIView):
    serializer_class = ChatSerializer
    name = 'room'
    permission_classes = [IsAuthenticatedOrReadOnly]

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
