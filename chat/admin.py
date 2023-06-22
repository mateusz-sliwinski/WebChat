from django.contrib import admin
from .models import Contact, ChatMessage, Chat

admin.site.register(Contact)
admin.site.register(Chat)
admin.site.register(ChatMessage)
