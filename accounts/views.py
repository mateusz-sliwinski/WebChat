"""Views files."""
# Django
from django.db.models import Q

# 3rd-party
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

# Project
from accounts.models import Friendship
from accounts.models import Users
from accounts.serializers import AddFriendshipSerializer
from accounts.serializers import FriendshipSerializer
from accounts.serializers import UpdateFriendshipSerializer
from accounts.serializers import UsersListSerializers
from accounts.serializers import UsersSerializers
from chat.models import Chat
from chat.models import Participant


class FriendshipCreate(CreateAPIView):  # noqa D101
    # Adding a new object to friendship and if it exists, replacing it
    queryset = Friendship.objects.all()
    serializer_class = AddFriendshipSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        one = request.data.get('from_user')
        two = request.data.get('to_user')
        qs = Friendship.objects.filter(Q(from_user__id=one) & Q(to_user__id=two) |
                                       Q(from_user__id=two) & Q(to_user__id=one))
        if qs.count() == 1:
            obj = qs.first()
            obj.delete()
        return self.create(request, *args, **kwargs)


class GetUserFriendship(ListAPIView):  # noqa D101
    # list of friends list
    serializer_class = UpdateFriendshipSerializer
    name = 'list_friendship'
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> dict:  # noqa D102
        user = self.request.user.id
        user_friends = Friendship.objects.filter(
            Q(from_user=user, status='Accepted') | Q(to_user=user, status='Accepted'))
        return user_friends


class PendingFriendship(CreateAPIView, ListAPIView):  # noqa D101
    # list of users who user can accept/reject
    serializer_class = UpdateFriendshipSerializer
    name = 'pending_friendship'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.GET.get('username')
        invs = Friendship.objects.filter(to_user__username=user).filter(status='Pending')
        return invs


class UpdateFriendship(RetrieveUpdateAPIView):  # noqa D101
    # accept invitations and create chat for both or reject/delete
    queryset = Friendship.objects.all()
    serializer_class = AddFriendshipSerializer
    name = 'update_friendship'
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if self.request.data.get('status') == 'Accepted':
            from_user = request.data['from_user']
            to_user = request.data['to_user']
            chat = Chat.objects.create()
            chat.save()
            Participant.objects.create(user=Users.objects.filter(id=from_user).get(), chat=chat)
            Participant.objects.create(user=Users.objects.filter(id=to_user).get(), chat=chat)
        return self.update(request, *args, **kwargs)


class BlockedFriendship(ListAPIView):  # noqa D101
    serializer_class = FriendshipSerializer
    name = 'blocked_friendship'
    permission_classes = [IsAuthenticated]

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
    # Returns a list of all users who are not in a relationship and with a status of Rejected
    serializer_class = UsersListSerializers
    name = 'list'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        uuid = self.request.user.id
        friends = Friendship.objects.filter(Q(from_user__id=uuid) | Q(to_user__id=uuid)).exclude(status='Rejected')
        names = set()
        for f in friends:
            names.add(f.to_user.username)
            names.add(f.from_user.username)

        return Users.objects.exclude(username__in=names)