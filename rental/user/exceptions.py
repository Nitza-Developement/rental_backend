from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer
from settings.utils.exceptions import BadRequest400APIException


class ErrorUserWithEmailAlreadyExists(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"User with email {email} already exists"
        self.default_code = "user-001"


class ErrorUserInvalidEmail(APIException):

    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid email "{email}"'
        self.default_code = "user-002"


class ErrorUserInvalidName(APIException):

    def __init__(self, name_error_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Error in name: {name_error_message}"
        self.default_code = "user-003"


class ErrorUserInvalidPassword(APIException):

    def __init__(self, password_error_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Error in password: {password_error_message}"
        self.default_code = "user-005"


class ErrorUserInvalidProfilePicture(APIException):

    def __init__(self, image_error_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Error in profile picture: {image_error_message}"
        self.default_code = "user-006"


def validate_user_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if "email" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["email"][0]

        if error_detail.code == "unique":
            raise ErrorUserWithEmailAlreadyExists(serializer.data.get("email"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorUserInvalidEmail(serializer.data.get("email"))

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]
        raise ErrorUserInvalidName(str(error_detail))

    if "password" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["password"][0]
        raise ErrorUserInvalidPassword(str(error_detail))

    if "image" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["image"][0]
        raise ErrorUserInvalidProfilePicture(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
