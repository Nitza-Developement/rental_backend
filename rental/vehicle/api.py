from rest_framework import status
from rest_framework.views import APIView
from settings.utils.api import APIViewWithPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
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
)
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateVehicleView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            vehicles_list = get_vehicles(tenant=request.user.defaultTenantUser().tenant.id)
            paginator = self.pagination_class()
            paginated_vehicles = paginator.paginate_queryset(vehicles_list, request)
            serialized_list = VehicleListSerializer(paginated_vehicles, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = VehicleCreateSerializer(data=request.data)
        print(f"{request.data}")
        if serializer.is_valid():
            created_vehicle = create_vehicle(
                tenant=request.user.defaultTenantUser().tenant,
                **serializer.validated_data,
            )
            serialized_vehicle = VehicleListSerializer(created_vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest400APIException(serializer.errors)


class GetUpdateAndDeleteVehicleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, search_by):
        try:
            vehicle = get_vehicle(search_by)
            serialized_vehicle = VehicleListSerializer(vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def put(self, request, vehicle_id):
        serializer = VehicleUpdateSerializer(
            data={
                "id": vehicle_id,
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
            }
        )
        if serializer.is_valid():
            updated_vehicle = update_vehicle(**serializer.validated_data)
            serialized_vehicle = VehicleListSerializer(updated_vehicle)
            return Response(serialized_vehicle.data, status=status.HTTP_200_OK)
        else:
            raise BadRequest400APIException(serializer.errors)

    def delete(self, request, vehicle_id):
        delete_vehicle(vehicle_id)
        return Response(status=status.HTTP_200_OK)
