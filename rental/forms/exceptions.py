from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorFormWithNameAlreadyExists(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Form with name {name} already exists"
        self.default_code = "form-001"


class ErrorFormInvalidName(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid name "{name}"'
        self.default_code = "form-002"


class ErrorCardWithNameAlreadyExists(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Card with name {name} already exists"
        self.default_code = "card-001"


class ErrorCardInvalidName(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid name "{name}"'
        self.default_code = "card-002"


class ErrorFieldWithNameAlreadyExists(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Field with name {name} already exists"
        self.default_code = "field-001"


class ErrorFieldInvalidName(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid name "{name}"'
        self.default_code = "field-002"


class ErrorFieldInvalidType(APIException):

    def __init__(self, type: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid type "{type}"'
        self.default_code = "field-003"


class ErrorCheckOptionWithNameAlreadyExists(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"CheckOption with name {name} already exists"
        self.default_code = "check-option-001"


class ErrorCheckOptionInvalidName(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid name "{name}"'
        self.default_code = "check-option-002"


class ErrorFieldResponseInvalidNote(APIException):

    def __init__(self, note: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid note "{note}"'
        self.default_code = "field-response-001"


class ErrorFieldResponseInvalidContent(APIException):

    def __init__(self, content: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid note "{content}"'
        self.default_code = "field-response-002"


class ErrorFieldResponseInvalidChecked(APIException):

    def __init__(self, checked: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid note "{checked}"'
        self.default_code = "field-response-003"


def validate_forms_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]

        if error_detail.code == "unique":
            raise ErrorFormWithNameAlreadyExists(serializer.data.get("name"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorFormInvalidName(serializer.data.get("name"))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))


def validate_card_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]

        if error_detail.code == "unique":
            raise ErrorCardWithNameAlreadyExists(serializer.data.get("name"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorCardInvalidName(serializer.data.get("name"))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))


def validate_field_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]

        if error_detail.code == "unique":
            raise ErrorFieldWithNameAlreadyExists(serializer.data.get("name"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorFieldInvalidName(serializer.data.get("name"))
    
    if "type" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["type"][0]

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorFieldInvalidType(serializer.data.get("type"))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
