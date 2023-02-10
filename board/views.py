import http

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Users
from board.models import Post, Comment, PostLikes
from board.permissions import IsOwnerOrReadOnly
from board.serializers import PostSerializer, CommentSerializer, PostLikeSerializer


class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class LikeListCreate(APIView):
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeSerializer
    name = 'Like'

    def post(self, request, post_id) -> Response:  # noqa  D102
        post = Post.objects.get(pk=post_id)
        if PostLikes.objects.filter(like_post=post, like_users=request.user).exists():
            PostLikes.objects.filter(like_post=post, like_users=request.user).delete()
        else:
            PostLikes.objects.create(like_post=post, like_users=request.user)
        return Response(status=status.HTTP_201_CREATED)
