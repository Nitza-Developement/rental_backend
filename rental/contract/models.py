from django.db import models
from rental.tenant.models import Tenant
from rental.client.models import Client
from rental.vehicle.models import Vehicle
from rental.rentalPlan.models import RentalPlan


class Contract(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='contracts')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='contracts')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='contracts')
    rental_plan = models.ForeignKey(RentalPlan, on_delete=models.CASCADE, related_name='contracts')
    creation_date = models.DateTimeField(auto_now=True)
    active_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.tenant} | {self.client} | {self.vehicle}'


class StageUpdate(models.Model):
    PENDING = 'Pending'
    ACTIVE = 'Active'
    ENDED = 'Ended'
    DISMISS = 'Dismiss'

    STAGE_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (ENDED, 'Ended'),
        (DISMISS, 'Dismiss'),
    ]

    date = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    previous_stage = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_stages')
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='stages_updates')


    def __str__(self) -> str:
        return f'{self.stage} | {self.date} | Previous: {self.previous_stage}'