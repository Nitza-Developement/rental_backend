from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    PolymorphicProxySerializer, OpenApiResponse
)
from rest_framework import status
from rest_framework.response import Response
from settings.utils.api import APIViewWithPagination
from rental.tenant.permissions import IsAdminTenant
from rest_framework.permissions import IsAuthenticated
from rental.tenant.features import (
    create_tenant,
    get_tenants,
    get_tenant,
    update_tenant,
    delete_tenant,
)
from rental.tenant.serializer import (
    CreateTenantSerializer,
    TenantSerializer,
    UpdateTenantSerializer,
)
from rental.tenant.exceptions import (
    validate_tenant_and_handle_errors,
    ErrorTenantWithEmailAlreadyExists,
    ErrorTenantInvalidEmail,
    ErrorTenantInvalidName,
)
from settings.utils.exceptions import (
    BadRequest400APIException,
    Unauthorized401APIException,
    NotFound404APIException
)


class ListAndCreateTenantsView(APIViewWithPagination):

    permission_classes = [IsAuthenticated, IsAdminTenant]

    def get_permissions(self):
        if self.request.method in ["GET"]:

            return [IsAuthenticated()]

        return super().get_permissions()

    @extend_schema(
        tags=['tenant'],
        parameters=[
            OpenApiParameter(name='searchText', type=str, description='Matches content in `name` and `email` fields, ignoring case ', required=False),
            OpenApiParameter(name='orderBy', type=str, description='You can select between `name`, `email` and `pk`', required=False),
            OpenApiParameter(name='asc', type=str, description='Ascending (`True`) or descending (`False`) order', required=False),
        ],
        responses={
            200: TenantSerializer(many=True),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response()
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        Endpoint for listing TenantUser
        """
        search_text = request.query_params.get("searchText", None)
        order_by = request.query_params.get("orderBy", "name")
        asc = request.query_params.get("asc", None)

        try:
            tenants_list = get_tenants(
                search_text=search_text,
                order_by=order_by,
                asc=False if asc == "False" else True,
            )

            paginator = self.pagination_class()
            paginated_tenants = paginator.paginate_queryset(tenants_list, request)
            serialized_list = TenantSerializer(paginated_tenants, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        tags=['tenant'],
        request = CreateTenantSerializer,
        responses={
            201: TenantSerializer,
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response()

        }
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator role.

        Endpoint for creating a Tenant.
        """
        serializer = CreateTenantSerializer(data=request.data)
        validate_tenant_and_handle_errors(serializer)

        created_tenant = create_tenant(
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
            isAdmin=serializer.validated_data["isAdmin"],
        )

        serialized_tenant = TenantSerializer(created_tenant)

        return Response(serialized_tenant.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteATenantView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminTenant]

    @extend_schema(
        responses={
            200: TenantSerializer,
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response(),
        }
    )
    def get(self, request, tenant_id=None):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator role.

        Endpoint to get an instance of Tenant
        """
        tenant = get_tenant(tenant_id)

        serialized_tenant = TenantSerializer(tenant)

        return Response(serialized_tenant.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UpdateTenantSerializer(),
        responses={
            200: TenantSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestTenant",
                serializers=[
                    ErrorTenantWithEmailAlreadyExists.schema_serializers(),
                    ErrorTenantInvalidEmail.schema_serializers(),
                    ErrorTenantInvalidName.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def put(self, request, tenant_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator role.

        Endpoint for editing a Tenant.

        If the value of `ownerId` is passed, the corresponding tenan-user will
        acquire the role of `Owner` and change the role of the previous
        tenan-user from `Owner` to `Staff`.
        """
        serializer = UpdateTenantSerializer(
            data={
                "id": tenant_id,
                "name": request.data.get("name"),
                "email": request.data.get("email"),
                "isAdmin": request.data.get("isAdmin"),
                "ownerId": request.data.get("ownerId"),
            }
        )
        validate_tenant_and_handle_errors(serializer)

        updated_tenant = update_tenant(
            tenant_id=tenant_id,
            name=serializer.validated_data.get("name"),
            email=serializer.validated_data.get("email"),
            isAdmin=serializer.validated_data.get("isAdmin"),
            ownerId=serializer.validated_data.get("ownerId"),
        )
        serialized_tenant = TenantSerializer(updated_tenant)

        return Response(serialized_tenant.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Successful response"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def delete(self, request, tenant_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator
        or owner role.

        Endpoint to delete a TenantUser.
        """
        delete_tenant(tenant_id)
        return Response(status=status.HTTP_200_OK)
