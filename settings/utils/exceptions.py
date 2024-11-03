from traceback import format_tb

from django.core.exceptions import ValidationError
from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from settings.utils.logging import log_error


def default_api_exception_handler(exc: Exception, context):
    if isinstance(exc, APIException):
        error_response = Response()
        error_response.content_type = "application/json"
        error_response.status_code = exc.status_code
        error_response.data = {
            "error": {
                "code": exc.default_code,
                "detail": exc.detail if exc.detail else exc.default_detail,
            }
        }
        return error_response

    # Log the exception
    traceback_call_list = format_tb(exc.__traceback__)
    full_call_stack = "".join(traceback_call_list)
    log_error(f"Traceback: {full_call_stack}")

    raise exc


class BadRequest400APIException(APIException):

    def __init__(self, detail: str):
        super().__init__(detail)
        self.status_code = HTTP_400_BAD_REQUEST
        self.default_detail = detail
        self.default_code = "bad_request"

    class BadRequest400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(response=BadRequest400APIException.BadRequest400Schema)

    @staticmethod
    def schema_serializers():
        return BadRequest400APIException.BadRequest400Schema()


class NotFound404APIException(APIException):

    def __init__(self, detail: str):
        super().__init__(detail)
        self.status_code = HTTP_404_NOT_FOUND
        self.default_detail = detail
        self.default_code = "not_found"

    class NotFound404Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(response=NotFound404APIException.NotFound404Schema)


class Unauthorized401APIException(APIException):

    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(detail)
        self.status_code = HTTP_401_UNAUTHORIZED
        self.default_detail = detail
        self.default_code = "unauthorized"

    class Unauthorized401Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=Unauthorized401APIException.Unauthorized401Schema
        )


class InternalServerError500APIException(APIException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(detail)
        self.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        self.default_detail = detail
        self.default_code = "internal_server_error"

    class InternalServerError500Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=InternalServerError500APIException.InternalServerError500Schema
        )

