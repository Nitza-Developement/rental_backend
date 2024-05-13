from rental.toll.models import TollDue
from settings.utils.exceptions import NotFound404APIException


def get_toll_dues():
    toll_dues = TollDue.objects.all()
    return toll_dues


def get_toll_due(toll_due_id: str):
    try:
        toll_due = TollDue.objects.get(id=toll_due_id)
    except TollDue.DoesNotExist:
        raise NotFound404APIException(f'Toll due with id {toll_due_id} not found')

    return toll_due


def create_toll_due(
    amount: int,
    plate: str,
    contract: str,
    stage: str,
    invoice: str = None,
    invoice_number: str = None,
    note: str = None
):

    new_toll_due = TollDue.objects.create(
        amount=amount,
        plate=plate,
        contract=contract,
        stage=stage,
        invoice=invoice,
        invoiceNumber=invoice_number,
        note=note
    )
    new_toll_due.save()
    return new_toll_due


def update_toll_due(
    toll_due_id: str,
    amount: int = None,
    plate: str = None,
    contract: str = None,
    stage: str = None,
    invoice: str = None,
    invoice_number: str = None,
    note: str = None
):
    try:
        toll_due = TollDue.objects.get(id=toll_due_id)
    except TollDue.DoesNotExist:
        raise NotFound404APIException(f'Toll due with id {toll_due_id} not found')

    if amount:
        toll_due.amount = amount
    if plate:
        toll_due.plate = plate
    if contract:
        toll_due.contract = contract
    if stage:
        toll_due.stage = stage
    if invoice:
        toll_due.invoice = invoice
    if invoice_number:
        toll_due.invoiceNumber = invoice_number
    if note:
        toll_due.note = note

    toll_due.full_clean()
    toll_due.save()
    return toll_due


def delete_toll_due(toll_due_id):
    try:
        toll_due = TollDue.objects.get(id=toll_due_id)
        toll_due.delete()
    except TollDue.DoesNotExist:
        raise NotFound404APIException(f'Toll due with id {toll_due_id} not found')
