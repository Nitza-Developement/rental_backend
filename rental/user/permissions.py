from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id=request.data.get("id")
        return user_id and str(user_id) == str(request.user.id)
