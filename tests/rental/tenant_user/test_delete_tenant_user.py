import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rental.tenantUser.models import TenantUser
from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase
from tests.rental.auth.utils.custom_test_user import CustomTestUser
from tests.rental.tenant_user.mixins.tenant_user_mixin import TenantUserMixin
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)

User = get_user_model()


class TestDeleteTenantUser(AuthAPITestCase, TenantUserMixin):
    def setUp(self):
        super().setUp()
        self.one_tenant_user: CustomTenantTestUser = self.create_tenant_user()

        self.multiple_tenant_user = self.create_tenant_user(tenant_quantity=3)

        custom_tenan_test_user = self.create_tenant_user()
        self.owner = CustomTestUser(
            user=custom_tenan_test_user.default_tenant_user.user,
            password=custom_tenan_test_user.password,
        )

    def call_tenant_user_delete(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenantUser-actions", args=[entity_id])
        response = self.client.delete(URL)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tenant_user(self):
        # case not loguin, response 401
        self.call_tenant_user_delete(
            entity_id=self.one_tenant_user.default_tenant_user.id,
            unauthorized=True,
        )

        # case not admin or owner, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_tenant_user_delete(
            entity_id=self.one_tenant_user.default_tenant_user.id,
            forbidden=True,
        )

        # case not found, response 404
        self.login(custom_user=self.owner)
        self.put_authentication_in_the_header()
        not_found_id = 999999
        self.call_tenant_user_delete(
            entity_id=not_found_id,
            not_found=True,
        )

        # case one tenant user, delete user too, response 200
        tenant_user_id = self.one_tenant_user.default_tenant_user.id
        user_id = self.one_tenant_user.default_tenant_user.user.id
        self.assertEqual(
            True, TenantUser.objects.filter(id=tenant_user_id).exists()
        )
        self.assertEqual(True, User.objects.filter(id=user_id).exists())
        self.call_tenant_user_delete(
            entity_id=self.one_tenant_user.default_tenant_user.id,
        )
        self.assertEqual(
            False, TenantUser.objects.filter(id=tenant_user_id).exists()
        )
        self.assertEqual(False, User.objects.filter(id=user_id).exists())

        # case multiple tenant user, remove default, reponse 200
        # automatically sets default to true to the next available
        tenant_user_default_old = self.multiple_tenant_user.list_tenant_user[0]
        tenant_user_default_old_id = tenant_user_default_old.id
        tenant_user_default_now = self.multiple_tenant_user.list_tenant_user[1]
        self.assertEqual(
            True,
            TenantUser.objects.filter(id=tenant_user_default_old_id).exists(),
        )
        self.assertEqual(
            True,
            TenantUser.objects.filter(id=tenant_user_default_now.id).exists(),
        )
        self.assertEqual(True, tenant_user_default_old.is_default)
        self.assertEqual(False, tenant_user_default_now.is_default)
        self.call_tenant_user_delete(
            entity_id=tenant_user_default_old_id,
        )
        tenant_user_default_now.refresh_from_db()
        self.assertEqual(
            False,
            TenantUser.objects.filter(id=tenant_user_default_old_id).exists(),
        )
        self.assertEqual(
            True,
            TenantUser.objects.filter(id=tenant_user_default_now.id).exists(),
        )
        self.assertEqual(True, tenant_user_default_now.is_default)

        # case multiple tenant user, remove not default, reponse 200
        tenant_user_too_delete_id = self.multiple_tenant_user.list_tenant_user[
            2
        ].id
        self.assertEqual(
            True,
            TenantUser.objects.filter(id=tenant_user_too_delete_id).exists(),
        )
        self.assertEqual(True, tenant_user_default_now.is_default)
        self.call_tenant_user_delete(
            entity_id=tenant_user_too_delete_id,
        )
        tenant_user_default_now.refresh_from_db()
        self.assertEqual(
            False,
            TenantUser.objects.filter(id=tenant_user_too_delete_id).exists(),
        )
        self.assertEqual(
            True,
            TenantUser.objects.filter(id=tenant_user_default_now.id).exists(),
        )
        self.assertEqual(True, tenant_user_default_now.is_default)
