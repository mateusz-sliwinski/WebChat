"""Models files."""
# Django
from django.db import models

# Project
from accounts.models import Users
from accounts.models import UUIDMixin


class Post(UUIDMixin, models.Model):  # noqa: D101
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(blank=True, null=True)
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(Users, related_name='posts', on_delete=models.CASCADE)

    class Meta:  # noqa: D106
        ordering = ['created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self) -> str:  # noqa: D105
        return f'{self.title} {self.created} '


class Comment(UUIDMixin, models.Model):  # noqa: D101
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    owner = models.ForeignKey(Users, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:  # noqa: D106
        ordering = ['created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:  # noqa: D105
        return f'{self.post.title}'


class PostLikes(UUIDMixin, models.Model):  # noqa: D101
    like_users = models.ForeignKey(Users, related_name='like_user', on_delete=models.CASCADE)
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
