from django.db import models
from rental.models import Tenant, TenantUser


class ContractFormTemplate(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(TenantUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.JSONField(null=True, blank=True, default=dict)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"
