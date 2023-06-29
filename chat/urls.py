# chat/urls.py
# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    path("chat/", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
]