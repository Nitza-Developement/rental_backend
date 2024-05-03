from rest_framework import status
from rest_framework.response import Response
from settings.utils.api import APIViewWithPagination
from rental.tenant.permissions import IsAdminTenant
from rest_framework.permissions import IsAuthenticated
from rental.tenant.features import create_tenant, get_tenants, get_tenant, update_tenant, delete_tenant
from rental.tenant.serializer import CreateTenantSerializer, TenantSerializer, UpdateTenantSerializer
from rental.tenant.exceptions import validate_tenant_and_handle_errors
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateTenantsView(APIViewWithPagination):

    permission_classes = [IsAuthenticated, IsAdminTenant]

    def get(self, request):
        search_text = request.query_params.get('searchText', None)
        order_by = request.query_params.get('orderBy', 'name')
        asc = request.query_params.get('asc', None)

        try:
            tenants_list = get_tenants(
                search_text=search_text,
                order_by=order_by,
                asc=False if asc == 'False' else True
            )

            paginator = self.pagination_class()
            paginated_tenants = paginator.paginate_queryset(tenants_list, request)
            serialized_list = TenantSerializer(paginated_tenants, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateTenantSerializer(data=request.data)
        validate_tenant_and_handle_errors(serializer)

        created_tenant = create_tenant(
            email=serializer.validated_data['email'],
            name=serializer.validated_data['name'],
            isAdmin=serializer.validated_data['isAdmin'],
        )

        serialized_tenant = TenantSerializer(created_tenant)

        return Response(serialized_tenant.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteATenantView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminTenant]

    def get(self, request, tenant_id=None):
        tenant = get_tenant(tenant_id)

        serialized_tenant = TenantSerializer(tenant)

        return Response(serialized_tenant.data, status=status.HTTP_200_OK)

    def put(self, request, tenant_id):
        serializer = UpdateTenantSerializer(data={
            'id': tenant_id,
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'isAdmin': request.data.get('isAdmin'),
        })
        validate_tenant_and_handle_errors(serializer)

        updated_tenant = update_tenant(
            tenant_id=tenant_id,
            name=serializer.validated_data.get('name'),
            email=serializer.validated_data.get('email'),
            isAdmin=serializer.validated_data.get('isAdmin'),
        )
        serialized_tenant = TenantSerializer(updated_tenant)

        return Response(serialized_tenant.data, status=status.HTTP_200_OK)

    def delete(self, request, tenant_id):
        delete_tenant(tenant_id)
        return Response(status=status.HTTP_200_OK)