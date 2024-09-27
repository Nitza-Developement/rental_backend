from drf_spectacular.utils import OpenApiResponse
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorPlanWithNameAlreadyExists(APIException):

    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Plan with name {name} already exists"
        self.default_code = "rental-plan-001"

    class ErrorPlanWithNameAlreadyExists400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorPlanWithNameAlreadyExists.ErrorPlanWithNameAlreadyExists400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorPlanWithNameAlreadyExists.ErrorPlanWithNameAlreadyExists400Schema()

class ErrorPlanInvalidName(APIException):

    def __init__(self, name_error_message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Error in name: {name_error_message}"
        self.default_code = "rental-plan-002"

    class ErrorPlanInvalidName400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorPlanInvalidName.ErrorPlanInvalidName400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorPlanInvalidName.ErrorPlanInvalidName400Schema()

class ErrorPlanInvalidAmount(APIException):

    def __init__(self, amount: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid amount "{amount}"'
        self.default_code = "rental-plan-003"

    class ErrorPlanInvalidAmount400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorPlanInvalidAmount.ErrorPlanInvalidAmount400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorPlanInvalidAmount.ErrorPlanInvalidAmount400Schema()


class ErrorPlanInvalidPeriodicity(APIException):

    def __init__(self, periodicity: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid periodicity "{periodicity}"'
        self.default_code = "rental-plan-004"

    class ErrorPlanInvalidPeriodicity400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorPlanInvalidPeriodicity.ErrorPlanInvalidPeriodicity400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorPlanInvalidPeriodicity.ErrorPlanInvalidPeriodicity400Schema()


def validate_plan_and_handle_errors(serializer: serializers.Serializer):

    serializer.is_valid()

    if "name" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["name"][0]

        if error_detail.code == "unique":
            raise ErrorPlanWithNameAlreadyExists(serializer.data.get("name"))

        if error_detail.code in ["invalid", "required", "blank"]:
            raise ErrorPlanInvalidName(serializer.data.get("name"))

    if "amount" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["amount"][0]
        raise ErrorPlanInvalidAmount(str(error_detail))

    if "periodicity" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["periodicity"][0]
        raise ErrorPlanInvalidPeriodicity(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
