"""Views files."""
# Django
from django.db.models import Q
import requests

from django.http import QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.http import JsonResponse

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
from accounts.serializers import FriendshipSerializer, UsersListSerializers, AddFriendshipSerializer, \
    UpdateFriendshipSerializer
from accounts.serializers import UsersSerializers
from chat.models import Chat, Participant


class FriendshipCreate(CreateAPIView):  # noqa D101
    queryset = Friendship.objects.all()
    serializer_class = AddFriendshipSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        one = request.data.get('from_user')
        two = request.data.get('to_user')
        print(one)
        print(two)
        print('post')
        return self.create(request, *args, **kwargs)


class FriendshipList(ListAPIView):  # noqa D101
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        print('get')
        return self.list(request, *args, **kwargs)



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
    #list of friends list
    serializer_class = UpdateFriendshipSerializer
    name = 'list_friendship'
    permission_classes = [AllowAny]

    def get_queryset(self) -> dict:  # noqa D102
        uuid = self.request.GET.get('pk')
        print(uuid)
        user = Users.objects.get(id=uuid)
        user_friends = Friendship.objects.filter(
            Q(from_user=uuid, status='Accepted') | Q(to_user=uuid, status='Accepted')
        )

        return user_friends


class PendingFriendship(CreateAPIView, ListAPIView):  # noqa D101
    #list of users who user can accept/reject
    serializer_class = UpdateFriendshipSerializer
    name = 'pending_friendship'
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.GET.get('username')
        invs = Friendship.objects.filter(to_user__username=user).filter(status='Pending')
        return invs


class UpdateFriendship(RetrieveUpdateAPIView):  # noqa D101
    queryset = Friendship.objects.all()
    serializer_class = AddFriendshipSerializer
    name = 'update_friendship'
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        # accept invitations and create chat for both
        from_user = request.data['from_user']
        to_user = request.data['from_user']
        print(from_user)
        chat = Chat.objects.create()
        chat.save()
        Participant.objects.create(user=Users.objects.filter(id=from_user).get(), chat=chat)
        Participant.objects.create(user=Users.objects.filter(id=to_user).get(), chat=chat)
        return self.update(request, *args, **kwargs)


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
    permission_classes = [AllowAny]

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
