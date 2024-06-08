from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


from rental.forms.features import get_forms, import_forms, create_form
from rental.forms.serializer import FormSerializer


class FormListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            forms_list = get_forms(request.user.defaultTenantUser().tenant)
            paginator = self.pagination_class()
            paginated_clients = paginator.paginate_queryset(forms_list, request)
            serialized_list = FormSerializer(paginated_clients, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):

        serializer = FormSerializer(data=request.data)

        if serializer.is_valid():

            created_form = create_form(
                request.user.defaultTenantUser().tenant,
                serializer.validated_data,
            )
            serialized_form = FormSerializer(created_form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormImportView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        serializer = FormSerializer(data=request.data, many=True)

        if serializer.is_valid():

            created_forms = import_forms(
                request.user.defaultTenantUser().tenant, serializer.validated_data
            )
            serialized_forms = FormSerializer(created_forms, many=True)

            return Response(serialized_forms.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
