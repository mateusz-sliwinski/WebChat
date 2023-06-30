"""Urls files."""
# Django
from django.urls import path

# 3rd-party
from rest_framework.urlpatterns import format_suffix_patterns

# Project
from board.views import CommentDetail
from board.views import CommentList
from board.views import LikeListCreate
from board.views import PostDetail
from board.views import PostList

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<uuid:pk>/', PostDetail.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<uuid:pk>/', CommentDetail.as_view()),
    path('like/<uuid:post_id>', LikeListCreate.as_view(), name='like'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
