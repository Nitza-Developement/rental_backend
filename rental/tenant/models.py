from django.db import models
from django.core.exceptions import ValidationError


def user_name_validator(name: str):
    if name.strip().isspace() or name.strip() == '':
        raise ValidationError(
            message='Name cannot be empty',
            code='invalid')


class Tenant(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,
                            validators=[user_name_validator])
    date_joined = models.DateTimeField(auto_now=True)
    isAdmin = models.BooleanField(default=False)
    
    @classmethod
    def get_adminTenant(cls):
        try:
            return cls.objects.filter(isAdmin=True).first()
        except cls.DoesNotExist:
            return None

    def get_adminTenantUsers_in_adminTenant(self):
        adminTenant = self.get_adminTenant()
        if adminTenant is not None:
            return self.tenantUsers.filter(tenant=adminTenant, role='Admin')
        return []
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['date_joined']

