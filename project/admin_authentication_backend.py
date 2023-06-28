from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Jeśli użytkownik nie istnieje, możesz wykonać odpowiednie działania, np. zalogować nieudaną próbę logowania.
            return None

        if not user.is_active:
            # Jeśli użytkownik jest nieaktywny, możesz wykonać odpowiednie działania, np. zalogować nieudaną próbę logowania.

            return None

        if user.check_password(password):
            # Hasło jest prawidłowe, można przeprowadzić dodatkowe działania, jeśli to konieczne.
            return user
        else:
            # Jeśli hasło jest nieprawidłowe, możesz wykonać odpowiednie działania, np. zalogować nieudaną próbę logowania.
            return None
