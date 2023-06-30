"""Permissions files."""
# 3rd-party
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):  # noqa: D101
    def has_object_permission(self, request, view, obj) -> bool | object:  # noqa: D102
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
