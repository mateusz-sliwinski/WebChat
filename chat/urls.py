from django.urls import path
from chat.views import ChatAPIView

urlpatterns = [
    path('api/chat/<str:room_name>/', ChatAPIView.as_view(), name='chat_api'),
]