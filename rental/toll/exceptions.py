from rest_framework import status
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorTollDueWithSameInvoiceAlreadyExists(APIException):
    def __init__(self, invoice: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Toll due with invoice "{invoice}" already exists'
        self.default_code = "toll_due-001"


class ErrorTollDueInvalidInvoice(APIException):
    def __init__(self, invoice: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid invoice "{invoice}"'
        self.default_code = "toll_due-002"


class ErrorTollDueInvalidAmount(APIException):
    def __init__(self, amount: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid amount "{amount}"'
        self.default_code = "toll_due-003"


def validate_toll_due_and_handle_errors(serializer):
    serializer.is_valid()

    if "invoice" in serializer.errors:
        error_detail = serializer.errors["invoice"][0]
        if error_detail.code == "unique":
            raise ErrorTollDueWithSameInvoiceAlreadyExists(
                serializer.data.get("invoice")
            )
        elif error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorTollDueInvalidInvoice(serializer.data.get("invoice"))

    if "amount" in serializer.errors:
        error_detail = serializer.errors["amount"][0]
        raise ErrorTollDueInvalidAmount(serializer.data.get("amount"))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
