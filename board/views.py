"""Views files."""
# 3rd-party
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

# Project
from board.models import Comment
from board.models import Post
from board.models import PostLikes
from board.permissions import IsOwnerOrReadOnly
from board.serializers import CommentSerializer
from board.serializers import PostLikeSerializer
from board.serializers import PostSerializer


class PostList(ListCreateAPIView):  # noqa: D101
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer) -> None:  # noqa: D102
        serializer.save(owner=self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):  # noqa: D101
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentList(ListCreateAPIView):  # noqa: D101
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):  # noqa: D102
        serializer.save(owner=self.request.user)


class CommentDetail(RetrieveUpdateDestroyAPIView):  # noqa: D101
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class LikeListCreate(APIView):  # noqa: D101
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
