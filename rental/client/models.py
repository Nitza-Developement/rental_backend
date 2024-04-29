from django.db import models
from rental.models import Tenant


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='clients')
