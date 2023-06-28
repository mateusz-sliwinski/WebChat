"""Urls.py files."""

# Django
import django
from django.urls import path
from django.urls import re_path
from django.utils.encoding import force_str

# 3rd-party
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import LoginView
from dj_rest_auth.views import LogoutView
from dj_rest_auth.views import PasswordChangeView
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.views import PasswordResetView
from dj_rest_auth.views import UserDetailsView

# Project
from accounts.views import BlockedFriendship
from accounts.views import DeleteFriendship
from accounts.views import FriendshipCreate
from accounts.views import GetUserFriendship
from accounts.views import PendingFriendship
from accounts.views import UpdateFriendship

django.utils.encoding.force_text = force_str

urlpatterns = [
    path(
        'account-confirm-email/<str:key>/',
        ConfirmEmailView.as_view(),
        name='verify_mail',
    ),
    path(
        'register/',
        RegisterView.as_view(),
        name='register',
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'verify-email/',
        VerifyEmailView.as_view(),
        name='rest_verify_email',
    ),
    path(
        'account-confirm-email/',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent',
    ),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        VerifyEmailView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'user/password/reset/',
        PasswordResetView.as_view(),
        name='rest_password_reset',
    ),

    path(
        'user/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'password/change/',
        PasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'user/<uuid:pk>',
        UserDetailsView.as_view(),
    ),
    path(
        'token/refresh/',
        get_refresh_view().as_view(),
        name='token_refresh',
    ),
    path(
        'friends/',
        FriendshipCreate.as_view(),
        name='friends',
    ),
    path(
        'friends/update/<uuid:pk>',
        UpdateFriendship.as_view(),
        name='friends_update',
    ),
    path(
        'friends/list/',
        GetUserFriendship.as_view(),
        name='friends_list',
    ),
    path(
        'friends/pending/',
        PendingFriendship.as_view(),
        name='friends_pending',
    ),
    path(
        'friends/blocked/',
        BlockedFriendship.as_view(),
        name='blocked_pending',
    ),
    path(
        'friends/delete/<uuid:pk>',
        DeleteFriendship.as_view(),
        name='blocked_pending',
    ),
]
