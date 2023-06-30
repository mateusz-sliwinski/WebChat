import logging

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logging.critical(f"Failed login attempt for a non-existent user: {username} {password}")
            return None

        if not user.is_active:
            logging.critical(f"Attempting to log in to an inactive user: {username}")
            return None

        if user.check_password(password):
            logging.critical(f"Successful user login: : {username}")
            return user
        else:
            logging.critical(f"Attempting to log in to a user with a bad password: {username} {password}")
            return None
