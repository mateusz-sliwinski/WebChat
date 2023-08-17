"""Admin backend custom files."""
# Standard Library
import logging.config

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Project
from project.settings import LOGGING_ADMIN

previous_logging_config = logging.getLogger().level
previous_logging_handlers = logging.getLogger().handlers[:]

logging.config.dictConfig(LOGGING_ADMIN)
logger_admin = logging.getLogger(__name__)


class CustomModelBackend(ModelBackend):  # noqa D101
    def authenticate(self, request, username=None, password=None, **kwargs) -> object | None:  # noqa D102
        User = get_user_model()

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            logger_admin.critical(
                f'Failed login attempt for a non-existent user: {username} {password}',
            )
            logging.getLogger().handlers = previous_logging_handlers
            logging.getLogger().setLevel(previous_logging_config)
            return None

        if not user.is_active:
            logger_admin.critical(f'Attempting to log in to an inactive user: {username}')
            logging.getLogger().handlers = previous_logging_handlers
            logging.getLogger().setLevel(previous_logging_config)
            return None

        if user.check_password(password):
            logger_admin.critical(f'Successful user login: : {username}')
            logging.getLogger().handlers = previous_logging_handlers
            logging.getLogger().setLevel(previous_logging_config)
            return user
        else:
            logger_admin.critical(
                f'Attempting to log in to a user with a bad password: {username} {password}',
            )
            logging.getLogger().handlers = previous_logging_handlers
            logging.getLogger().setLevel(previous_logging_config)
            return None
