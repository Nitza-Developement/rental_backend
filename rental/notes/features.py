from django.db.models import Q
from rental.notes.models import Note
from settings.utils.exceptions import NotFound404APIException


def get_notes(contract):
    notes = Note.objects.filter(
        Q(contract__id__icontains=contract)
    )
    return notes


def get_note(note_id: str):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise NotFound404APIException(f"Note with id {note_id} not found")

    return note


def create_note(
    contract: str,
    user: str,
    subject: str,
    body: str,
    remainder: str = None,
    file: str = None,
):

    new_note = Note.objects.create(
        contract=contract,
        user=user,
        subject=subject,
        body=body,
        remainder=remainder,
        file=file,
    )
    new_note.save()
    return new_note


def update_note(
    note_id: str,
    contract: str = None,
    user: str = None,
    subject: str = None,
    body: str = None,
    remainder: str = None,
    file: str = None,
):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise NotFound404APIException(f"Note with id {note_id} not found")

    if contract:
        note.contract = contract
    if user:
        note.user = user
    if subject:
        note.subject = subject
    if body:
        note.body = body
    if remainder:
        note.remainder = remainder
    if file:
        note.file = file

    note.full_clean()
    note.save()
    return note


def delete_note(note_id):
    try:
        note = Note.objects.get(id=note_id)
        note.delete()
    except Note.DoesNotExist:
        raise NotFound404APIException(f"Note with id {note_id} not found")
