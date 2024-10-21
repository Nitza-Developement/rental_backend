from datetime import datetime

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rental.contract.exceptions import validate_and_handle_errors
from rental.contract.features import create_contract
from rental.contract.features import create_stage_update
from rental.contract.features import get_contract
from rental.contract.features import get_contract_history
from rental.contract.features import get_contracts
from rental.contract.features import update_contract
from rental.contract.models import Contract
from rental.contract.serializer import ContractCreateSerializer
from rental.contract.serializer import ContractSerializer
from rental.contract.serializer import ContractUpdateSerializer
from rental.contract.serializer import StageUpdateCreateSerializer
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateContractView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request: Request):
        try:
            tenant = request.user.defaultTenantUser().tenant
            contract_list = get_contracts(tenant)

            if "plate" in request.query_params and request.query_params["plate"]:
                contract_list = contract_list.filter(
                    vehicle__plates__id=int(request.query_params["plate"]),
                )

            if "date" in request.query_params and request.query_params["date"]:
                date = datetime.strptime(
                    str(request.query_params["date"]),
                    "%Y-%m-%d",
                )
                contract_list = contract_list.filter(
                    Q(
                        Q(end_date=None) | Q(end_date__gte=date),
                    )
                    & Q(
                        Q(active_date__lte=date),
                    ),
                )

            paginator = self.pagination_class()
            paginated_contracts = paginator.paginate_queryset(contract_list, request)
            serialized_list = ContractSerializer(paginated_contracts, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = ContractCreateSerializer(data=request.data)
        validate_and_handle_errors(serializer)

        contract = create_contract(
            tenant=request.user.defaultTenantUser().tenant, **serializer.validated_data
        )
        create_stage_update(contract=contract)

        serialized_contract = ContractSerializer(contract)
        return Response(serialized_contract.data, status=status.HTTP_201_CREATED)


class GetUpdatePatchContractView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, contract_id):
        contract = get_contract(contract_id)

        serialized_contract = ContractSerializer(contract)

        return Response(serialized_contract.data, status=status.HTTP_200_OK)

    def put(self, request, contract_id):
        contract = Contract.objects.filter(id=contract_id).first()
        serializer = ContractUpdateSerializer(
            contract,
            data={
                "client": request.data.get("client"),
                "vehicle": request.data.get("vehicle"),
                "rental_plan": request.data.get("rental_plan"),
            },
        )
        validate_and_handle_errors(serializer)

        updated_contract = update_contract(contract_id, **serializer.validated_data)
        serialized_contract = ContractSerializer(updated_contract)
        return Response(serialized_contract.data, status=status.HTTP_200_OK)

    def patch(self, request, contract_id):
        serializer = StageUpdateCreateSerializer(
            data={
                "reason": request.data.get("reason"),
                "comments": request.data.get("comments"),
                "stage": request.data.get("stage"),
            }
        )
        validate_and_handle_errors(serializer)
        contract = get_contract(contract_id)
        create_stage_update(contract=contract, **serializer.validated_data)
        contract = get_contract(
            contract_id
        )  # This is to update the contract after changed the stage
        serialized_contract = ContractSerializer(contract)
        return Response(serialized_contract.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrStaffTenantUser])
def get_contract_timeline(request, contract_id):
    history_data = get_contract_history(contract_id)

    return Response(history_data, status=status.HTTP_200_OK)
