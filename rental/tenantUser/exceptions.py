from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorTenantUserInvalidRole(APIException):

    def __init__(self, invalid_role_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid role: {invalid_role_message}'
        self.default_code = 'tenant_user-001'


def validate_tenantUser_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if 'role' in serializer.errors:

        error_detail: ErrorDetail = serializer.errors['role'][0]

        if error_detail.code == 'invalid_choice':
            raise ErrorTenantUserInvalidRole(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
