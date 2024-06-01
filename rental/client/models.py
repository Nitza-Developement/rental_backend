from django.db import models
from rental.tenant.models import Tenant


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="clients")

    def __str__(self) -> str:
        return f"{self.name} | {self.email} | {self.phone_number}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["name"]
