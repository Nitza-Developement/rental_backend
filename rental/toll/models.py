from django.db import models
from rental.contract.models import Contract
from rental.vehicle.models import VehiclePlate


class TollDue(models.Model):
    PAID = "Paid"
    UNPAID = "Unpaid"

    STAGE_CHOICES = [(PAID, "Paid"), (UNPAID, "Unpaid")]

    amount = models.IntegerField()
    plate = models.ForeignKey(
        VehiclePlate, on_delete=models.CASCADE, related_name="toll_dues"
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="toll_dues"
    )
    stage = models.CharField(max_length=6, choices=STAGE_CHOICES)
    invoice = models.CharField(max_length=255, null=True, blank=True)
    invoiceNumber = models.CharField(max_length=255, null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.plate} | {self.amount} | {self.stage}"

    class Meta:
        verbose_name = "TollDue"
        ordering = ["createDate"]
