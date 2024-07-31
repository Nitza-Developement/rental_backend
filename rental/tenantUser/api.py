from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rental.tenantUser.swagger_serializer import TenantUserCreateSwaggerRepresentationSerializer
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from rental.tenantUser.permissions import IsAdminTenantUser
from settings.utils.exceptions import (
    BadRequest400APIException,
    Unauthorized401APIException,
    NotFound404APIException,
    InternalServerError500APIException,
)
from rental.tenantUser.exceptions import validate_tenantUser_and_handle_errors, ErrorTenantUserInvalidRole
from rental.tenantUser.serializer import (
    TenantUserListSerializer,
    TenantUserCreateSerializer,
    TenantUserUpdateSerializer,
)
from rental.tenantUser.features import (
    delete_tenantUser,
    get_tenantUser,
    get_tenantUsers,
    create_tenantUser,
    update_tenantUser,
)
from settings.utils.pagination import DefaultPagination


class ListAndCreateTenantUserView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminTenantUser]

    @extend_schema(
        responses={
            200: DefaultPagination.paginated_response_schema(TenantUserListSerializer(many=True)),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response(),
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator
        or owner role.

        Endpoint for listing TenantUser
        """
        try:
            tenant_users_list = get_tenantUsers(user_requesting=request.user)
            paginator = self.pagination_class()
            paginated_tenantUsers = paginator.paginate_queryset(
                tenant_users_list, request
            )
            serialized_list = TenantUserListSerializer(paginated_tenantUsers, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=TenantUserCreateSwaggerRepresentationSerializer(),
        responses={
            200: TenantUserListSerializer(),
            400: PolymorphicProxySerializer(
                                component_name="BadRequestTenantUser",
                                serializers=[
                                    ErrorTenantUserInvalidRole.schema_serializers(),
                                    BadRequest400APIException.schema_serializers(),
                                ],
                                resource_type_field_name="error"
                            ),
            401: Unauthorized401APIException.schema_response(),
            500: InternalServerError500APIException.schema_response()
        }
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator
        or owner role.

        Endpoint for creating a TenantUser.
        """
        serializer = TenantUserCreateSerializer(
            data={
                "role": request.data.get("role"),
                "tenant": request.data.get("tenant"),
                "is_default": request.data.get("is_default"),
            }
        )
        validate_tenantUser_and_handle_errors(serializer)

        try:
            created_tenantUser = create_tenantUser(
                email=request.data.get("email"),
                role=serializer.validated_data["role"],
                tenant=serializer.validated_data["tenant"],
                is_default=serializer.validated_data["is_default"],
            )

            serialized_tenantUser = TenantUserListSerializer(created_tenantUser)
            return Response(
                serialized_tenantUser.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as ex:
            raise BadRequest400APIException(str(ex.message))
        except Exception as ex:
            raise InternalServerError500APIException()


class GetUpdateAndDeleteTenantUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminTenantUser]


    @extend_schema(
        responses={
            200: TenantUserListSerializer(),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response(),
            500: InternalServerError500APIException.schema_response()
        }
    )
    def get(self, request, tenantUser_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator
        or owner role.

        Endpoint to get an instance of TenantUser
        """
        try:
            tenant_user = get_tenantUser(tenantUser_id)
            serialized_tenant_user = TenantUserListSerializer(tenant_user)
            return Response(serialized_tenant_user.data, status=status.HTTP_200_OK)
        except NotFound404APIException as e:
            raise e
        except Exception as e:
            raise InternalServerError500APIException(str(e))

    @extend_schema(
        request=TenantUserUpdateSerializer(),
        responses={
            200: TenantUserListSerializer(),
            400: PolymorphicProxySerializer(
                component_name="BadRequestTenantUser",
                serializers=[
                    ErrorTenantUserInvalidRole.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error"
            ),
            401: Unauthorized401APIException.schema_response()

        }
    )
    def put(self, request, tenantUser_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        Endpoint for editing a TenantUser.

        If the default entity status is changed to false, the default value is assigned
        to the next available entity.

        Therefore, this action can only be performed if there are more than one entity
        of this type.
        """
        serializer = TenantUserUpdateSerializer(data=request.data)
        validate_tenantUser_and_handle_errors(serializer)
        try:
            updated_tenant_user = update_tenantUser(
                tenant_user_id=tenantUser_id,
                is_default=serializer.validated_data.get("is_default"),
            )
            serialized_tenant_user = TenantUserListSerializer(updated_tenant_user)
            return Response(serialized_tenant_user.data, status=status.HTTP_200_OK)
        except ValidationError as ex:
            raise BadRequest400APIException(str(ex.message))
        except BadRequest400APIException as ex:
            raise ex
        except NotFound404APIException as ex:
            raise ex
        except Exception as ex:
            raise InternalServerError500APIException()
    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful response"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def delete(self, request, tenantUser_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator
        or owner role.

        Endpoint to delete a TenantUser.

        If the default entity status is deleted, the default value is assigned
        to the next available entity.

        If the default entity is deleted and there is no other available, then
        the user is also deleted.
        """
        delete_tenantUser(tenantUser_id)
        return Response(status=status.HTTP_200_OK)
