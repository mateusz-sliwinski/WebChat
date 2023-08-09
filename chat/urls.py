from django.urls import path, re_path
# from .views import (
#     ChatDetailView,
#     ChatListView,
#     ChatUpdateView,
#     ChatCreateView,
#     ChatDeletelView,
#
# )
from .views import ChatView
#
urlpatterns = [
    path('room/', ChatView.as_view(), name = ''),
    # path('create/', ChatCreateView.as_view()),
    # path('<int:pk>/', ChatDetailView.as_view()),
    # path('update/<int:pk>/', ChatUpdateView.as_view()),
    # path('delete/<int:pk>', ChatDeletelView.as_view()),
    # path('message/', MessageListView.as_view()),
]
