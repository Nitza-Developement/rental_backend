from django.db import models
from rental.tenant.models import Tenant


class RentalPlan(models.Model):
    WEEKLY = "Weekly"
    BIWEEKLY = "Biweekly"
    MONTHLY = "Monthly"

    PERIODICITY_CHOICES = [
        (WEEKLY, "Weekly"),
        (BIWEEKLY, "Biweekly"),
        (MONTHLY, "Monthly"),
    ]

    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="plans")

    def __str__(self) -> str:
        return f"{self.name} | {self.amount} | {self.periodicity}"

    class Meta:
        verbose_name = "Rental Plan"
        ordering = ["id"]
        unique_together = ("name", "periodicity", "amount", "tenant")
