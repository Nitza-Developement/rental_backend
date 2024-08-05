from rest_framework import permissions
from rental.tenant.models import Tenant


class IsAdminTenant(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.defaultTenantUser()
                and (
                        request.user.defaultTenantUser().tenant
                        == Tenant.objects.filter(isAdmin=True).first()
                    )
        )
