from django.db import models
from rental.user.models import User
from rental.tenant.models import Tenant


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

    def get_default_tenantUser(self):
        return self.tenantUsers.filter(is_default=True).first()

    def set_as_default(self):
        TenantUser.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

    class Meta:
        unique_together = ('user', 'is_default')

    User.add_to_class('defaultTenantUser', get_default_tenantUser)
    
    def get_user(self):
        return f'{self.user.email if self.user.name is None else self.user.name}'
    
    def get_tenant(self):
        return f'{self.tenant.name}'

    def __str__(self) -> str:
        return f'{self.id}'