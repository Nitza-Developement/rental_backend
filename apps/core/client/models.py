from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import Tenant


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, unique=True, validators=[
        RegexValidator(
            regex=r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$',
            message="Invalid Number!"
        )
    ])
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='clients')
