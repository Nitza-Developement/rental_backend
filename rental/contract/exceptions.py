from drf_spectacular.utils import OpenApiResponse
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorInvalidStage(APIException):

    def __init__(self, stage):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Invalid stage {stage}"
        self.default_code = "stage-001"

    class ErrorInvalidStage400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorInvalidStage.ErrorInvalidStage400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorInvalidStage.ErrorInvalidStage400Schema()



class ErrorInvalidDate(APIException):

    def __init__(self, date):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f"Invalid date {date}"
        self.default_code = "stage-002"

    class ErrorInvalidDate400Schema(serializers.Serializer):
        status_code = serializers.IntegerField()
        default_detail = serializers.CharField(allow_null=True)
        default_code = serializers.CharField(allow_null=True)

    @staticmethod
    def schema_response():
        return OpenApiResponse(
            response=ErrorInvalidDate.ErrorInvalidDate400Schema
        )

    @staticmethod
    def schema_serializers():
        return ErrorInvalidDate.ErrorInvalidDate400Schema()


def validate_and_handle_errors(serializer: serializers.Serializer):

    serializer.is_valid()

    if "stage" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["stage"][0]

        if error_detail.code == "invalid_choice":
            raise ErrorInvalidStage(serializer.data.get("stage"))

    if "date" in serializer.errors:

        error_detail: ErrorDetail = serializer.errors["stage"][0]

        if error_detail.code == "invalid":
            raise ErrorInvalidDate(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
