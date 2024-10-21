from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.toll.exceptions import validate_toll_due_and_handle_errors
from rental.toll.features import create_toll_due
from rental.toll.features import delete_toll_due
from rental.toll.features import get_toll_due
from rental.toll.features import get_toll_dues
from rental.toll.features import update_toll_due
from rental.toll.models import TollDue
from rental.toll.serializer import CreateTollDueSerializer
from rental.toll.serializer import TollDueSerializer
from rental.toll.serializer import UpdateTollDueSerializer
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateTollDuesView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            toll_dues_list = get_toll_dues()

            paginator = self.pagination_class()
            paginated_toll_dues = paginator.paginate_queryset(toll_dues_list, request)
            serialized_list = TollDueSerializer(paginated_toll_dues, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateTollDueSerializer(data=request.data)
        validate_toll_due_and_handle_errors(serializer)

        created_toll_due = create_toll_due(
            amount=serializer.validated_data["amount"],
            plate=serializer.validated_data["plate"],
            contract=serializer.validated_data["contract"],
            stage=serializer.validated_data["stage"],
            invoice=serializer.validated_data.get("invoice"),
            invoice_number=serializer.validated_data.get("invoiceNumber"),
            note=serializer.validated_data.get("note"),
        )

        serialized_toll_due = TollDueSerializer(created_toll_due)

        return Response(serialized_toll_due.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteATollDueView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, toll_due_id):
        toll_due = get_toll_due(toll_due_id)

        serialized_toll_due = TollDueSerializer(toll_due)

        return Response(serialized_toll_due.data, status=status.HTTP_200_OK)

    def put(self, request, toll_due_id):
        toll = TollDue.objects.filter(id=toll_due_id).first()
        serializer = UpdateTollDueSerializer(
            toll,
            data={
                "amount": request.data.get("amount"),
                "plate": request.data.get("plate"),
                "contract": request.data.get("contract"),
                "stage": request.data.get("stage"),
                "invoice": request.data.get("invoice"),
                "invoice_number": request.data.get("invoiceNumber"),
                "note": request.data.get("note"),
            },
        )
        validate_toll_due_and_handle_errors(serializer)

        updated_toll_due = update_toll_due(
            toll_due_id=toll_due_id,
            amount=serializer.validated_data.get("amount"),
            plate=serializer.validated_data.get("plate"),
            contract=serializer.validated_data.get("contract"),
            stage=serializer.validated_data.get("stage"),
            invoice=serializer.validated_data.get("invoice"),
            invoice_number=serializer.validated_data.get("invoiceNumber"),
            note=serializer.validated_data.get("note"),
        )
        serialized_toll_due = TollDueSerializer(updated_toll_due)

        return Response(serialized_toll_due.data, status=status.HTTP_200_OK)

    def delete(self, request, toll_due_id):
        delete_toll_due(toll_due_id)
        return Response(status=status.HTTP_200_OK)
