from rest_framework import permissions
from rental.tenant.models import Tenant

class IsAdminTenant(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.defaultTenantUser().tenant == Tenant.objects.filter(isAdmin = True).first():
            return True
        else:
            return False