from django.db import models
from rental.models import Tenant, TenantUser, Vehicle
from rental.forms.models import Form


class Inspection(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="inspections")
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="inspections"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="inspections"
    )
    tenantUser = models.ForeignKey(
        TenantUser, on_delete=models.CASCADE, related_name="inspections"
    )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.form.name
