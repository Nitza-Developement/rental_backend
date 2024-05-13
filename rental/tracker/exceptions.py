from rest_framework import status
from rest_framework.exceptions import APIException
from settings.utils.exceptions import BadRequest400APIException


class ErrorTrackerWithNameAlreadyExists(APIException):
    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Tracker with name "{name}" already exists'
        self.default_code = 'tracker-001'


class ErrorTrackerInvalidName(APIException):
    def __init__(self, name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid name "{name}"'
        self.default_code = 'tracker-002'


class ErrorTrackerHeartBeatDataInvalidTimestamp(APIException):
    def __init__(self, timestamp: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid timestamp "{timestamp}"'
        self.default_code = 'tracker_heartbeat_data-001'


def validate_tracker_and_handle_errors(serializer):
    serializer.is_valid()

    if 'name' in serializer.errors:
        error_detail = serializer.errors['name'][0]
        if error_detail.code == 'unique':
            raise ErrorTrackerWithNameAlreadyExists(serializer.data.get('name'))
        elif error_detail.code in ['invalid', 'required', 'blank']:
            raise ErrorTrackerInvalidName(serializer.data.get('name'))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))


def validate_tracker_heartbeat_data_and_handle_errors(serializer):
    serializer.is_valid()

    if 'timestamp' in serializer.errors:
        error_detail = serializer.errors['timestamp'][0]
        raise ErrorTrackerHeartBeatDataInvalidTimestamp(serializer.data.get('timestamp'))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
