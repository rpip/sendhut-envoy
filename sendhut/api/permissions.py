from rest_framework import permissions


class NoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
