"""Serializers files."""
# Standard Library
import logging

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder

# 3rd-party
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Project
from accounts.models import Friendship
from accounts.models import Users

logger = logging.getLogger(__name__)


class CustomRegisterSerializer(RegisterSerializer):  # noqa D101
    username = None
    first_name = serializers.CharField(required=True, label='First Name', max_length=254)
    last_name = serializers.CharField(required=True, label='Last Name', max_length=254)
    birth_date = serializers.DateField(required=True)

    def get_cleaned_data(self) -> dict:  # noqa D102
        data_dict = super().get_cleaned_data()
        data_dict['birth_date'] = self.validated_data.get('birth_date', '')
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        return data_dict


class CustomUserDetailsSerializer(UserDetailsSerializer):  # noqa D101
    class Meta(UserDetailsSerializer.Meta):  # noqa D102
        fields = UserDetailsSerializer.Meta.fields + \
                 (
                     'is_staff', 'birth_date', 'first_name', 'last_name', 'password',
                 )


class LoginSerializer(RestAuthLoginSerializer):  # noqa D100
    username = None


class CustomPasswordResetSerializer(PasswordResetSerializer):  # noqa D101
    def save(self):  # noqa D102
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

    def validate_email(self, value) -> serializers.ValidationError:  # noqa D102
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

    def get_email_options(self) -> dict:  # noqa D102
        return {
            'email_template_name': 'message/password_reset_message.txt',
        }


User = get_user_model()


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):  # noqa D101
    def validate(self, attrs: dict) -> dict:  # noqa D102
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs


class FriendshipSerializer(serializers.ModelSerializer):  # noqa D101
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    from_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
    )

    class Meta:  # noqa D106
        model = Friendship
        fields = ['id', 'status', 'from_user', 'to_user']

    def __init__(self, *args, **kwargs) -> None:  # noqa D107
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.user:
            self.fields['to_user'].queryset = self.fields['to_user'].queryset.exclude(
                id=request.user.id,
            )

            self.fields['from_user'].queryset = User.objects.filter(
                id=request.user.id,
            )

    def validate(self, data: dict) -> dict:  # noqa D105

        from_user = data.get('from_user').id
        to_user = data.get('to_user').id

        if Friendship.objects.filter(
                from_user=from_user,
                to_user=to_user,
                status='Blocked').exists():

            logger.info('User Try add blocked Friend')
            raise serializers.ValidationError('User 1 is blocked by user 2.')

        if Friendship.objects.filter(
                from_user=from_user,
                to_user=to_user,
                status='Accepted').exists():

            logger.info('user tried to add a friend he already had')
            raise serializers.ValidationError('User 1 is already an acquaintance of user 2.')

        return data


class UsersSerializers(serializers.ModelSerializer):  # noqa D101
    class Meta:  # noqa D106
        model = Users
        fields = ['first_name', 'last_name', 'last_login', 'date_joined', 'birth_date']
        extra_kwargs = {
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }

class UsersListSerializers(serializers.ModelSerializer):  # noqa D101
    class Meta:  # noqa D106
        model = Users
        fields = '__all__'
