from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from rental.contract.exceptions import validate_and_handle_errors
from rental.contract.serializer import ContractCreateSerializer, ContractUpdateSerializer, ContractSerializer, StageUpdateCreateSerializer
from rental.contract.features import create_contract, get_contract, get_contracts, update_contract, create_stage_update
from settings.utils.exceptions import BadRequest400APIException
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser


class ListAndCreateContractView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            contract_list = get_contracts()

            paginator = self.pagination_class()
            paginated_contracts = paginator.paginate_queryset(contract_list, request)
            serialized_list = ContractSerializer(paginated_contracts, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = ContractCreateSerializer(data=request.data)
        validate_and_handle_errors(serializer)

        contract = create_contract(**serializer.validated_data)
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
        serializer = ContractUpdateSerializer(data={
            'id': contract_id,
            'client': request.data.get('client'),
            'vehicle': request.data.get('vehicle'),
            'rental_plan': request.data.get('rental_plan')
        })
        validate_and_handle_errors(serializer)

        updated_contract = update_contract(contract_id, **serializer.validated_data)
        serialized_contract = ContractSerializer(updated_contract)
        return Response(serialized_contract.data, status=status.HTTP_200_OK)
    
    def patch(self, request, contract_id):
        serializer = StageUpdateCreateSerializer(data={
            'date': request.data.get('date'),
            'reason': request.data.get('reason'),
            'comments': request.data.get('comments'),
            'stage': request.data.get('stage')
        })
        validate_and_handle_errors(serializer)
        contract = get_contract(contract_id)
        create_stage_update(contract=contract,**serializer.validated_data)
        contract = get_contract(contract_id) #This is to update the contract after changed the stage
        serialized_contract = ContractSerializer(contract)
        return Response(serialized_contract.data, status=status.HTTP_200_OK)