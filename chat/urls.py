from django.urls import path, re_path

from .views import (
    ChatDetailView,
    ChatListView,
    ChatUpdateView,
    ChatCreateView,
    ChatDeletelView
)

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path('update/<pk>/', ChatUpdateView.as_view()),
    path('delete/<pk>', ChatDeletelView.as_view()),
]
