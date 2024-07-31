import json
from typing import Dict, List

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from ..auth.parent_case.auth_api_test_case import AuthAPITestCase
from ..auth.utils.custom_test_user import CustomTestUser
from .mixins.tenant_user_mixin import TenantUserMixin
from .utils.custom_tenant_test_user import CustomTenantTestUser

User = get_user_model()


class TestRetrieveTenantUser(AuthAPITestCase, TenantUserMixin):
    def setUp(self):
        super().setUp()
        self.list_tenant_user: List[CustomTenantTestUser] = [
            self.create_tenant_user() for _ in range(2)
        ]
        self.owner = CustomTestUser(
            user=self.list_tenant_user[0].default_tenant_user.user,
            password=self.list_tenant_user[0].password,
        )

    def call_tenant_user_retrieve(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Dict:
        URL = reverse("tenantUser-actions", args=[entity_id])
        response = self.client.get(URL)
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
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.validate_tenant_user_in_list(
            data=response_dict, tenant_user_id=entity_id
        )
        return response_dict

    def test_retrieve_tenant_user(self):
        self.call_tenant_user_retrieve(
            entity_id=self.list_tenant_user[0].default_tenant_user.id,
            unauthorized=True,
        )
        self.login(custom_user=self.owner)
        self.put_authentication_in_the_header()
        not_found_id = (
            self.list_tenant_user[0].default_tenant_user.id
            + self.list_tenant_user[1].default_tenant_user.id
        )
        self.call_tenant_user_retrieve(
            entity_id=not_found_id,
            not_found=True,
        )
        for custom_tenant_test_user in self.list_tenant_user:
            self.call_tenant_user_retrieve(
                entity_id=custom_tenant_test_user.default_tenant_user.id,
            )
