"""
WSGI config for WebChat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from accounts.models import Users

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

if not Users.objects.all():
    Users.objects.create_superuser(
        username='admin',
        email='admin@wp.pl',
        password='admin',
        is_active=True,
        is_staff=True,
    )
