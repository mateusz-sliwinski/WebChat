# Django
from django.contrib import admin
from .models import ChatMessage, Participant, Chat

admin.site.register(ChatMessage)
admin.site.register(Participant)
admin.site.register(Chat)

# Register your models here.
