"""Adapter files."""
# 3rd-party
from allauth.account.adapter import DefaultAccountAdapter

# Project
from accounts.models import Users
from project import settings


class CustomAccountAdapter(DefaultAccountAdapter):  # noqa D101

    def save_user(self, request, user, form, commit=False) -> object:  # noqa D102
        user = super().save_user(request, user, form, commit)
        count_user_first_name = Users.objects.filter(first_name=user.first_name).count()
        data = form.cleaned_data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.birth_date = data.get('birth_date')
        user.username = user.first_name + str(count_user_first_name)
        user.save()
        return user

    def send_mail(self, template_prefix, email, context) -> None:  # noqa D102
        context['activate_url'] = settings.FRONT_URL + \
                                  'account-confirm-email/' + context['key']

        msg = self.render_mail(template_prefix, email, context)
        msg.send()
