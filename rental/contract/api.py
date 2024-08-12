from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from rental.contract.swagger_serializer import ContractSwaggerRepresentationSerializer
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from rental.contract.exceptions import validate_and_handle_errors, ErrorInvalidStage, ErrorInvalidDate
from rental.contract.serializer import (
    ContractCreateSerializer,
    ContractUpdateSerializer,
    ContractSerializer,
    StageUpdateCreateSerializer,
)
from rental.contract.features import (
    create_contract,
    get_contract,
    get_contracts,
    update_contract,
    create_stage_update,
    get_contract_history
)
from settings.utils.exceptions import BadRequest400APIException, Unauthorized401APIException, NotFound404APIException
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser


class ListAndCreateContractView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):
        try:
            contract_list = get_contracts(request.user.defaultTenantUser().tenant)

            paginator = self.pagination_class()
            paginated_contracts = paginator.paginate_queryset(contract_list, request)
            serialized_list = ContractSerializer(paginated_contracts, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=ContractCreateSerializer(),
        responses={
            201: ContractSwaggerRepresentationSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestContract",
                serializers=[
                    ErrorInvalidStage.schema_serializers(),
                    ErrorInvalidDate.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_contract"
            ),
            401: Unauthorized401APIException.schema_response(),
        }
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for creating a Contract.
        """
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

    @extend_schema(
        request=ContractUpdateSerializer,
        responses={
            200: ContractSwaggerRepresentationSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestClient",
                serializers=[
                    ErrorInvalidStage.schema_serializers(),
                    ErrorInvalidDate.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_client"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def put(self, request, contract_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for editing a Contract.
        """
        serializer = ContractUpdateSerializer(
            data={
                "id": contract_id,
                "client": request.data.get("client"),
                "vehicle": request.data.get("vehicle"),
                "rental_plan": request.data.get("rental_plan"),
            }
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