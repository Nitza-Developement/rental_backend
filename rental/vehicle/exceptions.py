from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer
from settings.utils.exceptions import BadRequest400APIException


class ErrorVehicleTypeInvalid(APIException):
    def __init__(self, vehicle_type: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid vehicle type: {vehicle_type}'
        self.default_code = 'vehicle-001'


class ErrorVehicleUnavailable(APIException):
    def __init__(self, vehicle_id: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Vehicle with ID {vehicle_id} is unavailable'
        self.default_code = 'vehicle-002'


class ErrorVehicleVINInvalid(APIException):
    def __init__(self, vin: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid VIN: {vin}'
        self.default_code = 'vehicle-003'


class ErrorVehicleYearInvalid(APIException):
    def __init__(self, year: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid year: {year}'
        self.default_code = 'vehicle-004'


class ErrorVehicleMakeInvalid(APIException):
    def __init__(self, make: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid make: {make}'
        self.default_code = 'vehicle-005'


class ErrorVehicleModelInvalid(APIException):
    def __init__(self, model: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid model: {model}'
        self.default_code = 'vehicle-006'


class ErrorVehicleTrimInvalid(APIException):
    def __init__(self, trim: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid trim: {trim}'
        self.default_code = 'vehicle-007'


class ErrorVehicleOdometerInvalid(APIException):
    def __init__(self, odometer: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid odometer reading: {odometer}'
        self.default_code = 'vehicle-008'


class ErrorVehicleNicknameInvalid(APIException):
    def __init__(self, nickname: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid nickname: {nickname}'
        self.default_code = 'vehicle-009'


class ErrorVehicleSpareTiresInvalid(APIException):
    def __init__(self, spare_tires: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid number of spare tires: {spare_tires}'
        self.default_code = 'vehicle-010'


class ErrorVehicleExtraFieldsInvalid(APIException):
    def __init__(self, extra_fields: dict):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid extra fields: {extra_fields}'
        self.default_code = 'vehicle-011'


class ErrorVehicleStatusInvalid(APIException):
    def __init__(self, status: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.default_detail = f'Invalid status: {status}'
        self.default_code = 'vehicle-012'


def validate_vehicle_and_handle_errors(serializer: Serializer):
    serializer.is_valid()

    if 'type' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['type'][0]
        raise ErrorVehicleTypeInvalid(serializer.data.get('type'))

    if 'status' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['status'][0]
        raise ErrorVehicleUnavailable(serializer.data.get('id'))

    if 'vin' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['vin'][0]
        raise ErrorVehicleVINInvalid(serializer.data.get('vin'))

    if 'year' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['year'][0]
        raise ErrorVehicleYearInvalid(serializer.data.get('year'))

    if 'make' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['make'][0]
        raise ErrorVehicleMakeInvalid(serializer.data.get('make'))

    if 'model' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['model'][0]
        raise ErrorVehicleModelInvalid(serializer.data.get('model'))

    if 'trim' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['trim'][0]
        raise ErrorVehicleTrimInvalid(serializer.data.get('trim'))

    if 'odometer' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['odometer'][0]
        raise ErrorVehicleOdometerInvalid(serializer.data.get('odometer'))

    if 'nickname' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['nickname'][0]
        raise ErrorVehicleNicknameInvalid(serializer.data.get('nickname'))

    if 'spare_tires' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['spare_tires'][0]
        raise ErrorVehicleSpareTiresInvalid(serializer.data.get('spare_tires'))

    if 'extraFields' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['extraFields'][0]
        raise ErrorVehicleExtraFieldsInvalid(
            serializer.data.get('extraFields'))

    if 'status' in serializer.errors:
        error_detail: ErrorDetail = serializer.errors['status'][0]
        raise ErrorVehicleStatusInvalid(serializer.data.get('status'))

    if len(serializer.errors) > 0:
        raise BadRequest400APIException(str(serializer.errors))
