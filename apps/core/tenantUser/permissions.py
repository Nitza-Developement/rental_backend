from rest_framework import permissions
from apps.core.models import TenantUser

class IsAdminTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == TenantUser.ADMIN

class IsAdminOrStaffTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role in [TenantUser.ADMIN, TenantUser.STAFF]

class IsSelfOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.kwargs.get('user_id') == request.user.id or request.user.role == TenantUser.ADMIN
