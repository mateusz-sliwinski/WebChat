"""Serializers files."""
# 3rd-party
from rest_framework import serializers

# Project
from accounts.models import Users
from board.models import Comment
from board.models import Post
from board.models import PostLikes


class PostSerializer(serializers.ModelSerializer):  # noqa: D101
    owner = serializers.ReadOnlyField(source='owner.first_name')
    owner_last_name = serializers.ReadOnlyField(source='owner.last_name')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    like_post = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:  # noqa: D106
        model = Post
        fields = ['id', 'title', 'image', 'body', 'owner', 'owner_last_name', 'comments', 'like_post', 'created']


class UsersPostSerializer(serializers.ModelSerializer):  # noqa: D101
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:  # noqa: D106
        model = Users
        fields = ['id', 'username', 'posts', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')
    owner_last_name = serializers.ReadOnlyField(source='owner.last_name')

    class Meta:  # noqa: D106
        model = Comment
        fields = ['id', 'body', 'owner','owner_last_name', 'post']


class PostLikeSerializer(serializers.ModelSerializer):  # noqa: D101
    class Meta:  # noqa: D106
        model = PostLikes
        fields = '__all__'
