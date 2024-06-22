from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.forms.models import Form
from rental.models import Vehicle
from rental.inspections.serializer import (
    InspectionSerializer,
    CreateInspectionSerializer,
)
from rental.inspections.features import (
    get_inspections,
    create_inspection,
    get_inspection,
)

from rental.inspections.validators import validate_inspection_response


class InspectionListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            forms_list = get_inspections(request.user.defaultTenantUser().tenant)
            paginator = self.pagination_class()
            paginated_clients = paginator.paginate_queryset(forms_list, request)
            serialized_list = InspectionSerializer(paginated_clients, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):

        serializer = CreateInspectionSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            inspection = create_inspection(
                form=serializer.validated_data["form"],
                vehicle=serializer.validated_data["vehicle"],
                tenant=request.user.defaultTenantUser().tenant,
                tenantUser=request.user.defaultTenantUser(),
            )

            serialized_inspection = InspectionSerializer(inspection)
            return Response(serialized_inspection.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InspectionGetUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, inspection_id):

        inspection = get_inspection(
            inspection_id, request.user.defaultTenantUser().tenant
        )
        serialized_inspection = InspectionSerializer(inspection)

        return Response(serialized_inspection.data, status=status.HTTP_200_OK)


class FormsAndVehiclesGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):

        forms = Form.objects.filter(tenant=request.user.defaultTenantUser().tenant)
        vehicles = Vehicle.objects.filter(
            tenant=request.user.defaultTenantUser().tenant
        )

        return Response(
            {
                "forms": [{"value": form.id, "name": form.name} for form in forms],
                "vehicles": [
                    {"value": vehicle.id, "name": vehicle.nickname}
                    for vehicle in vehicles
                ],
            }
        )


class InspectionCreateResponseView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        validate_inspection_response(request.data.dict(), request)

        return Response("ok")

        # serializer = CreateInspectionResponseSerializer(
        #     data=request.data, context={"request": request}
        # )

        # if serializer.is_valid():

        #     return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
