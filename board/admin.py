# Django
from django.contrib import admin

# Project
from board.models import Comment
from board.models import Post
from board.models import PostLikes


@admin.register(Post)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(Comment)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(PostLikes)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass
