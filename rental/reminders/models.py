from auditlog.models import AuditlogHistoryField
from django.db import models

from rental.client.models import Client
from rental.contract.models import Contract
from rental.tenantUser.models import TenantUser
from rental.toll.models import TollDue
from rental.vehicle.models import Vehicle


def get_file_path(note, filename: str):
    return f"user/{note.created_by.id}/note/{note.id}/{filename}"


class Reminder(models.Model):
    WAITING = "Waiting"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    INCOMPLETE = "Incomplete"

    STATUS_CHOICES = [
        (WAITING, "Waiting"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed"),
        (INCOMPLETE, "Incomplete"),
    ]

    # Note fields
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=WAITING)
    important = models.BooleanField(default=False)
    title = models.TextField()
    content = models.TextField(null=True)
    remainder = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to=get_file_path, null=True, blank=True)

    # Meta data
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        TenantUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="my_reminders",
    )
    history = AuditlogHistoryField()

    # Links
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
    )
    toll_due = models.ForeignKey(
        TollDue,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
    )
