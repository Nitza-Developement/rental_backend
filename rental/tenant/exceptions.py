from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorTenantWithEmailAlreadyExists(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Tenant with email {email} already exists"
        self.default_code = "tenant-001"


class ErrorTenantInvalidEmail(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid email "{email}"'
        self.default_code = "tenant-002"


class ErrorTenantInvalidName(APIException):

    def __init__(self, name_error_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Error in name: {name_error_message}"
        self.default_code = "tenant-003"


def validate_tenant_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "email" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["email"][0]

        if error_detail.code == "unique":
            raise ErrorTenantWithEmailAlreadyExists(serializer.data.get("email"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorTenantInvalidEmail(serializer.data.get("email"))

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]
        raise ErrorTenantInvalidName(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
