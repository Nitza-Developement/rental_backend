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


class ContractFormField(models.Model):

    TEXT = "TEXT"
    NUMBER = "NUMBER"
    SIGNATURE = "SIGNATURE"
    EMAIL = "EMAIL"
    PHONE = "PHONE"

    FORM_FIELD_TYPES = (
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (SIGNATURE, "Signature"),
        (EMAIL, "Email"),
        (PHONE, "Phone"),
    )

    template = models.ForeignKey(
        ContractFormTemplate, on_delete=models.CASCADE, related_name="fields"
    )
    placeholder = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=FORM_FIELD_TYPES)
    required = models.BooleanField(default=True)


class ContractForm(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(TenantUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(
        ContractFormTemplate, on_delete=models.CASCADE, related_name="contracts"
    )
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]


class ContractFormFieldResponse(models.Model):
    form = models.ForeignKey(ContractForm, on_delete=models.CASCADE)
    field = models.ForeignKey(ContractFormField, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
