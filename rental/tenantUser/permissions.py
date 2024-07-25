from rest_framework import permissions
from rental.models import TenantUser


class IsAdminTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.defaultTenantUser() and (
            request.user.defaultTenantUser().role
            in (TenantUser.ADMIN, TenantUser.OWNER)
        )


class IsAdminOrStaffTenantUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.defaultTenantUser() and (
            request.user.defaultTenantUser().role
            in (TenantUser.ADMIN, TenantUser.STAFF, TenantUser.OWNER)
        )
