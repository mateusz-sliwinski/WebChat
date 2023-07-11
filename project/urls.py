"""WebChat URL Configuration."""

# Django
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

# Project
from project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('board/', include('board.urls')),
    path('chat/', include('chat.urls')),
    path('issue_tracking/', include('issue_tracking.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
