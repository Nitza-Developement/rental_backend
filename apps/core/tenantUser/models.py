from django.db import models
from apps.core.user.models import User
from apps.core.tenant.models import Tenant


class TenantUser(models.Model):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    OWNER = 'Owner'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (OWNER, 'Owner'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STAFF)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenantUsers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenantUsers')
    is_default = models.BooleanField(default=False)