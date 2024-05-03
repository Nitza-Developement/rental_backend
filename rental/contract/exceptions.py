from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException

class ErrorInvalidStage(APIException):

    def __init__(self, stage):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid stage {stage}'
        self.default_code = 'stage-001'

class ErrorInvalidDate(APIException):

    def __init__(self, date):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid date {date}'
        self.default_code = 'stage-002'

def validate_and_handle_errors(serializer: Serializer):

    serializer.is_valid()

    if 'stage' in serializer.errors:

        error_detail: ErrorDetail = serializer.errors['stage'][0]

        if error_detail.code == 'invalid':
            raise ErrorInvalidStage(serializer.data.get('stage'))

    if 'date' in serializer.errors:

        error_detail: ErrorDetail = serializer.errors['stage'][0]

        if error_detail.code == 'invalid':
            raise ErrorInvalidDate(str(error_detail))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))