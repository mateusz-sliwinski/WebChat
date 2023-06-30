# Django
from django.db.models import Q

# 3rd-party
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Project
from accounts.models import Friendship
from accounts.models import Users
from accounts.serializers import FriendshipSerializer
from accounts.serializers import UsersSerializers


class FriendshipCreate(ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateFriendship(RetrieveUpdateAPIView):
    serializer_class = FriendshipSerializer
    name = 'update_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(to_user=self.request.user.id)
        return queryset

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_invitations = request.data.get('status')
        'The logic for creating a chat room for a user who accepts their friend if it is "Accepted" during Update is ' \
            'to create a chat room'

        return Response(serializer.data)


class GetUserFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'list_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Accepted'))
        return queryset


class PendingFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'pending_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Pending'))
        return queryset


class BlockedFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'blocked_friendship'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Blocked'))
        return queryset


class DeleteFriendship(RetrieveDestroyAPIView):
    serializer_class = FriendshipSerializer
    name = 'delete_friendship'

    def get_queryset(self) -> dict:  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Accepted'))
        return queryset


class GetUserInformation(RetrieveUpdateAPIView):
    serializer_class = UsersSerializers
    name = 'profile'
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> dict:
        return Users.objects.filter(id=self.request.user.id)
