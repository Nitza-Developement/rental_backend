from django.db import models
from rental.user.models import User
from rental.contract.models import Contract


def get_file_path(note, filename: str):

    return f"tenant/{note.contract.tenant.id}/contract/{note.contract.id}/notes/{note.id}/{filename}"


class Note(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="notes"
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="notes")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    createdDate = models.DateTimeField(auto_now=True)
    remainder = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to="notes/", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.subject} | {self.body}"

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ["createdDate"]
