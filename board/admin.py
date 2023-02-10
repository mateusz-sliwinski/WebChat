from django.contrib import admin

from board.models import Post, Comment, PostLikes


@admin.register(Post)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(Comment)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass


@admin.register(PostLikes)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    pass
