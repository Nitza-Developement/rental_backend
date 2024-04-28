from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.tenantUser.serializer import TenantUserListSerializer, TenantUserCreateSerializer, TenantUserUpdateSerializer
from apps.core.tenantUser.features import delete_tenantUser, get_tenantUser, get_tenantUsers, create_tenantUser, update_tenantUser
from apps.core.tenantUser.exceptions import validate_tenantUser_and_handle_errors
from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException


class ListAndCreateTenantUserView(APIViewWithPagination):

    def get(self, request):
        try:
            tenant_users_list = get_tenantUsers()
            paginator = self.pagination_class()
            paginated_tenantUsers = paginator.paginate_queryset(tenant_users_list, request)
            serialized_list = TenantUserListSerializer(paginated_tenantUsers, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            return BadRequest400APIException(str(e))

    def post(self, request):
        serializer = TenantUserCreateSerializer(data=request.data)
        validate_tenantUser_and_handle_errors(serializer)

        created_tenantUser = create_tenantUser(
            email=serializer.validated_data['email'],
            role=serializer.validated_data['role'],
            tenant=serializer.validated_data['tenant'],
            is_default=serializer.validated_data['is_default']
        )

        serialized_tenantUser = TenantUserListSerializer(created_tenantUser)
        return Response(serialized_tenantUser.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteTenantUserView(APIView):

    def get(self, request, tenant_user_id):
        try:
            tenant_user = get_tenantUser(tenant_user_id)
            serialized_tenant_user = TenantUserListSerializer(tenant_user)
            return Response(serialized_tenant_user.data, status=status.HTTP_200_OK)
        except Exception as e:
            return BadRequest400APIException(str(e))

    def put(self, request, tenant_user_id):
        serializer = TenantUserUpdateSerializer(data=request.data)
        validate_tenantUser_and_handle_errors(serializer)

        updated_tenant_user = update_tenantUser(
            tenant_user_id=tenant_user_id,
            email=serializer.validated_data.get('email'),
            is_default=serializer.validated_data.get('is_default'),
            tenant=serializer.validated_data.get('tenant')
        )

        serialized_tenant_user = TenantUserListSerializer(updated_tenant_user)
        return Response(serialized_tenant_user.data, status=status.HTTP_200_OK)

    def delete(self, request, tenant_user_id):
        delete_tenantUser(tenant_user_id)
        return Response(status=status.HTTP_200_OK)
