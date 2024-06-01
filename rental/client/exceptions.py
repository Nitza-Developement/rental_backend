from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer
from settings.utils.exceptions import BadRequest400APIException


class ErrorClientWithEmailAlreadyExists(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Client with email {email} already exists"
        self.default_code = "client-001"


class ErrorClientWithPhoneNumberAlreadyExists(APIException):

    def __init__(self, phone_number: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Client with phone number {phone_number} already exists"
        self.default_code = "client-002"


class ErrorClientInvalidEmail(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid email "{email}"'
        self.default_code = "client-003"


class ErrorClientInvalidPhoneNumber(APIException):

    def __init__(self, phone_number: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid phone number "{phone_number}"'
        self.default_code = "client-004"


def validate_client_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "email" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["email"][0]

        if error_detail.code == "unique":
            raise ErrorClientWithEmailAlreadyExists(serializer.data.get("email"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorClientInvalidEmail(serializer.data.get("email"))

    if "phone_number" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["phone_number"][0]

        if error_detail.code == "unique":
            raise ErrorClientWithPhoneNumberAlreadyExists(
                serializer.data.get("phone_number")
            )

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorClientInvalidPhoneNumber(serializer.data.get("phone_number"))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
