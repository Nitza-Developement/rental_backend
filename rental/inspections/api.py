from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.forms.models import Form
from rental.models import Vehicle
from rental.inspections.serializer import InspectionSerializer
from rental.inspections.features import get_inspections


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

        # serializer = FormSerializer(data=request.data)

        # if serializer.is_valid():

        #     created_form = create_form(
        #         request.user.defaultTenantUser().tenant,
        #         serializer.validated_data,
        #     )
        #     serialized_form = FormSerializer(created_form)

        #     return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("ok")


class FormsAndVehiclesGet(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):

        forms = Form.objects.filter(tenant=request.user.defaultTenantUser().tenant)
        vehicles = Vehicle.objects.filter(
            tenant=request.user.defaultTenantUser().tenant
        )

        return Response(
            {
                "forms": [{"id": form.id, "name": form.name} for form in forms],
                "vehicles": [
                    {"id": vehicle.id, "name": vehicle.nickname} for vehicle in vehicles
                ],
            }
        )
