# Django
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accounts.models import Friendship
from accounts.serializers import FriendshipSerializer


class FriendshipList(ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateFriendship(UpdateAPIView):
    pass
