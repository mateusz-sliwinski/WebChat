"""Admin.py files."""
# Django
from django.contrib import admin

# Project
from accounts.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):  # noqa D101
    list_display = [
        'first_name',
        'last_name',
        'email',
    ]
    list_filter = [
        'last_name',
    ]
    list_display_links = (
        'email',
    )
    list_editable = [
        'first_name',
        'last_name',
    ]