from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.forms.features import (
    get_forms,
    get_form,
    import_forms,
    create_form,
    create_card,
    rename_form,
    delete_form,
    delete_card,
    update_card,
)
from rental.forms.serializer import FormSerializer, CardSerializer


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


class FormImportView(APIView):
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


class FormGetUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, form_id):

        form = get_form(form_id, request.user.defaultTenantUser().tenant)
        serialized_form = FormSerializer(form)

        return Response(serialized_form.data, status=status.HTTP_200_OK)

    def put(self, request, form_id):

        serializer = FormSerializer(data=request.data | {"id": form_id})

        if serializer.is_valid():
            rename_form(
                form_id,
                request.data.get("name"),
                request.user.defaultTenantUser().tenant,
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, form_id):
        delete_form(form_id, request.user.defaultTenantUser().tenant)
        return Response(status=status.HTTP_200_OK)


class CardCreateUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():

            form = get_form(
                request.data.get("form_id"), request.user.defaultTenantUser().tenant
            )

            card = create_card(
                form,
                serializer.validated_data.get("name"),
                serializer.validated_data.get("fields"),
            )

            serialized_card = CardSerializer(card)
            return Response(serialized_card.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, card_id):
        delete_card(card_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):

        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():

            card = update_card(
                request.data.get("id"),
                serializer.validated_data.get("name"),
                request.data.get("fields"),
            )
            serialized_card = CardSerializer(card)
            return Response(serialized_card.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
