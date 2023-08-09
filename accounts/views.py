"""Views files."""
# Django
from django.db.models import Q
import requests

from django.http import QueryDict

# 3rd-party
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Project
from accounts.models import Friendship
from accounts.models import Users
from accounts.serializers import FriendshipSerializer, UsersListSerializers, AddFriendshipSerializer
from accounts.serializers import UsersSerializers
from chat.models import Chat, Participant


class FriendshipCreate(ListCreateAPIView):  # noqa D101
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateFriendship(RetrieveUpdateAPIView):  # noqa D101
    serializer_class = FriendshipSerializer
    name = 'update_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(to_user=self.request.user.id)
        return queryset

    def update(self, request, *args, **kwargs) -> Response:  # noqa D102
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print('serializer sdsad', serializer)
        serializer.save()
        status_invitations = request.data.get('status')
        'The logic for creating a chat room for a user who accepts their friend if it is "Accepted" during Update is ' \
        'to create a chat room'

        return Response(serializer.data)


class CreateFriendship(CreateAPIView):  # noqa D101
    serializer_class = AddFriendshipSerializer
    name = 'create_friendship'
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # print(request.data)
        one = request.data.get('from_user')
        two = request.data.get('to_user')
        chat = Chat.objects.create()
        chat.save()
        Participant.objects.create(user=Users.objects.filter(id=one).get(), chat=chat)
        Participant.objects.create(user=Users.objects.filter(id=two).get(), chat=chat)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class GetUserFriendship(ListAPIView):  # noqa D101
    serializer_class = UsersListSerializers
    name = 'list_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        name_user = self.request.GET.get('username')
        user = Users.objects.get(username=name_user)
        friends = user.sender.all() | user.receiver.all()
        names = []
        for f in friends:
            if f.to_user.username not in names:
                names.append(f.to_user.username)
            if f.from_user.username not in names:
                names.append(f.from_user.username)
        return Users.objects.filter(username__in=names)


class PendingFriendship(ListAPIView):  # noqa D101
    serializer_class = FriendshipSerializer
    name = 'pending_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(
            Q(from_user=self.request.user.id) and Q(status='Pending'),
        )
        return queryset


class BlockedFriendship(ListAPIView):  # noqa D101
    serializer_class = FriendshipSerializer
    name = 'blocked_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(
            Q(from_user=self.request.user.id) and Q(status='Blocked'),
        )
        return queryset


class DeleteFriendship(RetrieveDestroyAPIView):  # noqa D101
    serializer_class = FriendshipSerializer
    name = 'delete_friendship'

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(
            Q(from_user=self.request.user.id) and Q(status='Accepted'),
        )
        return queryset


class GetUserInformation(RetrieveUpdateAPIView):  # noqa D101
    serializer_class = UsersSerializers
    name = 'profile'
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> dict:  # noqa D102
        return Users.objects.filter(id=self.request.user.id)


class UserList(ListAPIView):  # noqa D101

    serializer_class = UsersListSerializers
    name = 'list'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.GET.get('username')
        friends = Friendship.objects.filter(Q(from_user__username=user) | Q(to_user__username=user))
        names = []
        for f in friends:
            if f.to_user.username not in names:
                names.append(f.to_user.username)
            if f.from_user.username not in names:
                names.append(f.from_user.username)

        return Users.objects.exclude(username__in=names)
