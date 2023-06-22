from django.urls import path
from .views import (
    ChatListView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,
    ChatDetailView
)

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path('update/<pk>', ChatUpdateView.as_view()),
    path('delete/<pk>', ChatDeleteView.as_view()),
]
