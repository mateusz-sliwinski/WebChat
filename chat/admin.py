# Django
from django.contrib import admin

# Local
from .models import Chat
from .models import ChatMessage
from .models import Participant

admin.site.register(ChatMessage)
admin.site.register(Participant)
admin.site.register(Chat)
