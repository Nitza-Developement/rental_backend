from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from rental.vehicle.models import Vehicle
from rental.vehicle.swagger_seralizer import AuditlogVehicleSwaggerRepresentationSerializer
from settings.utils.api import APIViewWithPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rest_framework.decorators import api_view, permission_classes
from rental.vehicle.serializer import (
    VehicleListSerializer,
    VehicleCreateSerializer,
    VehicleUpdateSerializer,
)
from rental.vehicle.features import (
    get_vehicles,
    create_vehicle,
    get_vehicle,
    update_vehicle,
    delete_vehicle,
    get_vehicle_history,
)
from settings.utils.exceptions import BadRequest400APIException, Unauthorized401APIException, NotFound404APIException
from settings.utils.pagination import DefaultPagination


class ListAndCreateVehicleView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    @extend_schema(
        responses={
            200: DefaultPagination.paginated_response_schema(VehicleListSerializer(many=True)),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response()
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for listing Vehicle
        """
        try:
            vehicles_list = get_vehicles(
                tenant=request.user.defaultTenantUser().tenant.id
            )
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
        }
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for creating a Vehicle.
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

    @extend_schema(
        responses={
            200: VehicleListSerializer,
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response(),
        }
    )
    def get(self, request, vehicle_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint to get an instance of Vehicle
        """
        try:
            vehicle = get_vehicle(vehicle_id)
            serialized_vehicle = VehicleListSerializer(vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        except APIException as e:
            raise e
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=VehicleUpdateSerializer,
        responses={
            200: VehicleListSerializer,
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
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
            vehicle= Vehicle.objects.get(id=vehicle_id)
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
            instance=vehicle
        )
        if serializer.is_valid():
            updated_vehicle = update_vehicle(
                user=request.user, vehicle=vehicle,**serializer.validated_data
            )
            serialized_vehicle = VehicleListSerializer(updated_vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        else:
            raise BadRequest400APIException(serializer.errors)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful response"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def delete(self, request, vehicle_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint to delete a Vehicle.
        """
        delete_vehicle(vehicle_id)
        return Response(status=status.HTTP_200_OK)



@extend_schema_view(
    get=extend_schema(responses=AuditlogVehicleSwaggerRepresentationSerializer(many=True)),
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrStaffTenantUser])
def get_vehicle_timeline(request, vehicle_id):
    """
    This method requires the user to be authenticated in order to be used.
    Authentication is performed by using a JWT (JSON Web Token) that is included
    in the HTTP request header.

    This endpoint requires the authenticated user to have the administrator, staff
    or owner role.

    Returns a history of actions performed on a vehicle
    """
    history_data = get_vehicle_history(vehicle_id)

    return Response(history_data, status=status.HTTP_200_OK)
