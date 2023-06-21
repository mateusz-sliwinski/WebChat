# Django
from django.db.models import Q

# 3rd-party
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Project
from accounts.models import Friendship
from accounts.serializers import FriendshipSerializer


class FriendshipCreate(ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateFriendship(UpdateAPIView):
    serializer_class = FriendshipSerializer
    name = 'update_friendship'

    def get_queryset(self):  # noqa D102
        queryset = Friendship.objects.filter(to_user=self.request.user.id)
        return queryset


class GetUserFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'list_friendship'

    def get_queryset(self):  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Accepted'))
        return queryset


class PendingFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'pending_friendship'

    def get_queryset(self):  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Pending'))
        return queryset


class BlockedFriendship(ListAPIView):
    serializer_class = FriendshipSerializer
    name = 'blocked_friendship'

    def get_queryset(self):  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Blocked'))
        return queryset


class DeleteFriendship(RetrieveDestroyAPIView):
    serializer_class = FriendshipSerializer
    name = 'delete_friendship'

    def get_queryset(self):  # noqa D102
        queryset = Friendship.objects.filter(Q(from_user=self.request.user.id) and Q(status='Accepted'))
        return queryset
