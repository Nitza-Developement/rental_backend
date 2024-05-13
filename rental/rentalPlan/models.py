from django.db import models

class RentalPlan(models.Model):
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'

    PERIODICITY_CHOICES = [
        (WEEKLY, 'Weekly'),
        (BIWEEKLY, 'Biweekly'),
        (MONTHLY, 'Monthly')
    ]
    
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)

    def __str__(self) -> str:
        return f'{self.name} | {self.amount} | {self.periodicity}'

    class Meta:
        verbose_name = 'Rental Plan'
        ordering = ['id']
        unique_together = ('name', 'periodicity', 'amount')