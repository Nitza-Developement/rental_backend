from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rental.client.models import Client
from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.client.serializer import (
    ClientListSerializer,
    ClientCreateSerializer,
    ClientUpdateSerializer,
)
from rental.client.features import (
    delete_client,
    get_client,
    get_clients,
    create_client,
    update_client,
)
from rental.client.exceptions import validate_client_and_handle_errors, ErrorClientWithEmailAlreadyExists, \
    ErrorClientWithPhoneNumberAlreadyExists, ErrorClientInvalidEmail, ErrorClientInvalidPhoneNumber
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException, NotFound404APIException, Unauthorized401APIException
from settings.utils.utils_request_data import qdict_to_dict


class ClientListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    @extend_schema(
        responses={
            200: ClientListSerializer(many=True),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response()
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for listing Client
        """
        try:
            clients_list = get_clients(request.user.defaultTenantUser().tenant)
            paginator = self.pagination_class()
            paginated_clients = paginator.paginate_queryset(clients_list, request)
            serialized_list = ClientListSerializer(paginated_clients, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=ClientCreateSerializer(),
        responses={
            201: ClientListSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestClient",
                serializers=[
                    ErrorClientWithEmailAlreadyExists.schema_serializers(),
                    ErrorClientWithPhoneNumberAlreadyExists.schema_serializers(),
                    ErrorClientInvalidEmail.schema_serializers(),
                    ErrorClientInvalidPhoneNumber.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_client"
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

        Endpoint for creating a Client.
        """
        serializer = ClientCreateSerializer(data=request.data)
        validate_client_and_handle_errors(serializer)

        created_client = create_client(
            name=serializer.validated_data["name"],
            email=serializer.validated_data["email"],
            phone_number=serializer.validated_data["phone_number"],
            tenant=request.user.defaultTenantUser().tenant,
        )

        serialized_client = ClientListSerializer(created_client)
        return Response(serialized_client.data, status=status.HTTP_201_CREATED)


class ClientGetUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, client_id):
        try:
            client = get_client(client_id)
            serialized_client = ClientListSerializer(client)
            return Response(serialized_client.data, status=status.HTTP_200_OK)
        except APIException as e:
            raise e
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=ClientUpdateSerializer,
        responses={
            200: ClientListSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestClient",
                serializers=[
                    ErrorClientWithEmailAlreadyExists.schema_serializers(),
                    ErrorClientWithPhoneNumberAlreadyExists.schema_serializers(),
                    ErrorClientInvalidEmail.schema_serializers(),
                    ErrorClientInvalidPhoneNumber.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_client"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def put(self, request, client_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for editing a Client.
        """
        try:
            Client.objects.get(id=client_id)
        except (TypeError, ValueError, Client.DoesNotExist):
            raise NotFound404APIException(f"Client with id {client_id} doesnt exist")

        serializer = ClientUpdateSerializer(data=qdict_to_dict(request.data) | {"id": client_id})
        validate_client_and_handle_errors(serializer)

        updated_client = update_client(
            client_id=client_id,
            name=serializer.validated_data.get("name"),
            email=serializer.validated_data.get("email"),
            phone_number=serializer.validated_data.get("phone_number"),
        )

        serialized_client = ClientListSerializer(updated_client)
        return Response(serialized_client.data, status=status.HTTP_200_OK)

    def delete(self, request, client_id):
        delete_client(client_id)
        return Response(status=status.HTTP_200_OK)
