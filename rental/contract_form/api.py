from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.contract_form.serializer import ContractFormTemplateSerializer
from rental.contract_form.features import get_contract_form_templates


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

        return Response("ok")
