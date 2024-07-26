from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.contract_form.serializer import ContractFormTemplateSerializer

from rental.contract_form.features import (
    get_contract_form_templates,
    create_contract_form_template,
)


class ContractFormListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):

        tenant = request.user.defaultTenantUser().tenant
        paginator = self.pagination_class()

        try:
            forms_list = get_contract_form_templates(tenant)
            paginated_forms = paginator.paginate_queryset(forms_list, request)
            serialized_list = ContractFormTemplateSerializer(paginated_forms, many=True)

            return paginator.get_paginated_response(serialized_list.data)
        except Exception as error:
            raise BadRequest400APIException(str(error)) from error

    def post(self, request):

        serializer = ContractFormTemplateSerializer(data=request.data)

        if serializer.is_valid():

            form = create_contract_form_template(**serializer.validated_data)
            serialized_form = ContractFormTemplateSerializer(form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractFormGetUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, pk):

        return Response("ok")

    def put(self, request, pk):

        return Response("ok")

    def delete(self, request, pk):
        return Response("ok")
