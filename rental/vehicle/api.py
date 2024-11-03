from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.vehicle.features import create_vehicle
from rental.vehicle.features import delete_vehicle
from rental.vehicle.features import get_vehicle
from rental.vehicle.features import get_vehicle_history
from rental.vehicle.features import get_vehicles
from rental.vehicle.features import update_vehicle
from rental.vehicle.models import Vehicle
from rental.vehicle.models import VehiclePlate
from rental.vehicle.serializer import VehicleCreateSerializer
from rental.vehicle.serializer import VehicleListSerializer
from rental.vehicle.serializer import VehiclePlateSerializer
from rental.vehicle.serializer import VehicleUpdateSerializer
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException
from settings.utils.exceptions import NotFound404APIException
from settings.utils.exceptions import Unauthorized401APIException


class ListAndCreateVehicleView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    @extend_schema(
        responses={
            200: VehicleListSerializer(many=True),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for listing TenantUser
        """
        try:
            vehicles_list = get_vehicles(
                tenant=request.user.defaultTenantUser().tenant.id
            )

            if "all" in request.query_params and (
                request.query_params["all"] == "true"
                or request.query_params["all"] is True
            ):
                serialized_list = VehicleListSerializer(vehicles_list, many=True)
                return Response(serialized_list.data)

            paginator = self.pagination_class()
            paginated_vehicles = paginator.paginate_queryset(vehicles_list, request)
            serialized_list = VehicleListSerializer(paginated_vehicles, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=VehicleCreateSerializer(),
        responses={
            201: VehicleListSerializer,
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
        },
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for creating a TenantUser.
        """
        serializer = VehicleCreateSerializer(data=request.data)
        if serializer.is_valid():
            created_vehicle = create_vehicle(
                user=request.user,
                **serializer.validated_data,
            )
            serialized_vehicle = VehicleListSerializer(created_vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest400APIException(serializer.errors)


class GetUpdateAndDeleteVehicleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, vehicle_id):
        try:
            vehicle = get_vehicle(vehicle_id)
            serialized_vehicle = VehicleListSerializer(vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=VehicleUpdateSerializer,
        responses={
            200: VehicleListSerializer,
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response(),
        },
    )
    def put(self, request, vehicle_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for editing a Vehicle.
        """

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except (TypeError, ValueError, Vehicle.DoesNotExist):
            raise NotFound404APIException(f"Vehicle with id {vehicle_id} doesnt exist")

        serializer = VehicleUpdateSerializer(
            data={
                "type": request.data.get("type"),
                "year": request.data.get("year"),
                "make": request.data.get("make"),
                "model": request.data.get("model"),
                "trim": request.data.get("trim"),
                "vin": request.data.get("vin"),
                "odometer": request.data.get("odometer"),
                "nickname": request.data.get("nickname"),
                "spare_tires": request.data.get("spare_tires"),
                "extra_fields": request.data.get("extra_fields"),
                "status": request.data.get("status"),
                "plate": request.data.get("plate"),
            },
            instance=vehicle,
        )
        if serializer.is_valid():
            updated_vehicle = update_vehicle(
                user=request.user, vehicle=vehicle, **serializer.validated_data
            )
            serialized_vehicle = VehicleListSerializer(updated_vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        else:
            raise BadRequest400APIException(serializer.errors)

    def delete(self, request, vehicle_id):
        delete_vehicle(vehicle_id)
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrStaffTenantUser])
def get_vehicle_timeline(request, vehicle_id):
    history_data = get_vehicle_history(vehicle_id)

    return Response(history_data, status=status.HTTP_200_OK)


class VehiclePlateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request: Request):
        tenant = request.user.defaultTenantUser().tenant
        plates = VehiclePlate.objects.filter(vehicle__tenant=tenant)
        serializer = VehiclePlateSerializer(plates, many=True)
        return Response(serializer.data)
