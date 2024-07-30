import json
from typing import List

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from ..auth.parent_case.auth_api_test_case import AuthAPITestCase
from ..auth.utils.custom_test_user import CustomTestUser
from .mixins.tenant_user_mixin import TenantUserMixin
from .utils.custom_tenant_test_user import CustomTenantTestUser

User = get_user_model()


class TestUpdateTenantUser(AuthAPITestCase, TenantUserMixin):
    def setUp(self):
        super().setUp()
        self.list_one_tenant_user: List[CustomTenantTestUser] = [
            self.create_tenant_user() for _ in range(2)
        ]
        self.multiple_tenant_user = self.create_tenant_user(tenant_quantity=3)

        self.owner = CustomTestUser(
            user=self.list_one_tenant_user[0].default_tenant_user.user,
            password=self.list_one_tenant_user[0].password,
        )

    def call_update_tenant_user(
        self,
        entity_id: int,
        is_default: bool = True,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenantUser-actions", args=[entity_id])
        payload = {
            "is_default": is_default,
        }
        response = self.client.put(URL, payload)
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
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.validate_tenant_user_in_list(
            data=response_dict, tenant_user_id=entity_id
        )
        return response_dict

    def test_update_tenant_user(self):
        first_tenant_user = self.list_one_tenant_user[0]

        # case not loguin, response 401
        self.call_update_tenant_user(
            entity_id=first_tenant_user.default_tenant_user.id,
            unauthorized=True,
        )

        # case not admin or owner, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_update_tenant_user(
            entity_id=first_tenant_user.default_tenant_user.id, forbidden=True
        )

        # case not found, response 404
        self.login(custom_user=self.owner)
        self.put_authentication_in_the_header()
        not_found_id = 999999
        self.call_update_tenant_user(
            entity_id=not_found_id,
            not_found=True,
        )

        for custom_tenant_test_user in self.list_one_tenant_user:
            # case one tenant user, remove default, response 400
            self.call_update_tenant_user(
                entity_id=custom_tenant_test_user.default_tenant_user.id,
                is_default=False,
                bad_request=True,
            )

            # case one tenant user, ignore default to true, response 200
            self.call_update_tenant_user(
                entity_id=custom_tenant_test_user.default_tenant_user.id,
                is_default=True,
            )

        # case multiple tenant user, remove default, reponse 200
        # automatically sets default to true to the next available
        tenant_user_default_to_false = (
            self.multiple_tenant_user.list_tenant_user[0]
        )
        tenant_user_default_to_true = (
            self.multiple_tenant_user.list_tenant_user[1]
        )
        self.assertEqual(True, tenant_user_default_to_false.is_default)
        self.assertEqual(False, tenant_user_default_to_true.is_default)
        self.call_update_tenant_user(
            entity_id=tenant_user_default_to_false.id,
            is_default=False,
        )
        tenant_user_default_to_false.refresh_from_db()
        tenant_user_default_to_true.refresh_from_db()
        self.assertEqual(False, tenant_user_default_to_false.is_default)
        self.assertEqual(True, tenant_user_default_to_true.is_default)
