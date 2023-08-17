# Django
from django.urls import path

# Local
from .views import ChatView

urlpatterns = [
    path('room/', ChatView.as_view(), name='room'),
]
