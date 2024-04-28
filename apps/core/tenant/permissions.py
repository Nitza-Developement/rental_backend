from rest_framework import permissions

class IsAdminTenant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.isAdmin