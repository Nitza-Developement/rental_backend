from rest_framework import permissions
from apps.core.models import TenantUser

class IsAdminTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.defaultTenantUser().role == TenantUser.ADMIN
    

class IsAdminOrStaffTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.defaultTenantUser().role == TenantUser.ADMIN or request.user.defaultTenantUser().role == TenantUser.STAFF