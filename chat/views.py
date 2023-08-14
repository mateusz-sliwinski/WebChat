from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
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
from .models import Chat,Participant

User = get_user_model()

#
# def get_user_contact(username):
#     user = get_object_or_404(User, username=username)
#     contact = get_object_or_404(Contact, user=user)
#     return contact
#
#
class ChatView(ListAPIView):
    serializer_class = ChatSerializer
    name = 'room'
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.GET.get('username')
        current_user = self.request.GET.get('current_user')
        print(user)
        print(current_user)
        participants_from_user = Participant.objects.filter(user__username=current_user)
        participants_to_user = Participant.objects.filter(user__username=user)
        chat_id = None
        for participant_from in participants_from_user:
            for participant_to in participants_to_user:
                if participant_from.chat == participant_to.chat:
                    chat_id = participant_from.chat.id
        queryset = Chat.objects.filter(id=chat_id)
        return queryset
#
#
# class ChatDetailView(RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.AllowAny,)
#
#
# class ChatDeletelView(DestroyAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class ChatUpdateView(UpdateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class ChatCreateView(CreateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class MessageListView(ListAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = (permissions.IsAuthenticated,)
