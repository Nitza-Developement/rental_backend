from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rental.forms.features import clone_form
from rental.forms.features import create_card
from rental.forms.features import create_form
from rental.forms.features import delete_card
from rental.forms.features import delete_form
from rental.forms.features import get_form
from rental.forms.features import get_forms
from rental.forms.features import import_forms
from rental.forms.features import rename_form
from rental.forms.features import update_card
from rental.forms.models import Form
from rental.forms.serializer import CardSerializer
from rental.forms.serializer import FormSerializer
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class FormListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            forms_list = get_forms(request.user.defaultTenantUser().tenant)
            paginator = self.pagination_class()
            paginated_clients = paginator.paginate_queryset(forms_list, request)
            serialized_list = FormSerializer(paginated_clients, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as exc:
            raise BadRequest400APIException(str(exc)) from exc

    def post(self, request):

        serializer = FormSerializer(data=request.data)

        if serializer.is_valid():

            created_form = create_form(
                request.user.defaultTenantUser().tenant,
                serializer.validated_data,
            )
            serialized_form = FormSerializer(created_form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCloneView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        form = clone_form(
            request.data.get("form_id"), request.user.defaultTenantUser().tenant
        )

        serializer = FormSerializer(form)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardCreateUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request, form_id):

        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():

            form = get_form(form_id, request.user.defaultTenantUser().tenant)

            card = create_card(
                form,
                serializer.validated_data.get("name"),
                serializer.validated_data.get("fields"),
            )

            serialized_card = CardSerializer(card)
            return Response(serialized_card.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, form_id, card_id):
        delete_card(card_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, form_id, card_id):

        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():

            card = update_card(
                card_id,
                serializer.validated_data.get("name"),
                serializer.validated_data.get("fields"),
            )
            serialized_card = CardSerializer(card)
            return Response(serialized_card.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
