import json
from typing import Dict, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase
from tests.rental.tenant_user.mixins.tenant_user_mixin import TenantUserMixin
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)

User = get_user_model()


class TestListTenantUser(AuthAPITestCase, TenantUserMixin):
    def setUp(self):
        super().setUp()
        self.list_tenant_user = [self.create_tenant_user() for _ in range(20)]
        self.total_count = len(self.list_tenant_user) + 1
        self.maxDiff = None

    def call_tenant_user_list(
        self,
        len_list: int,
        expected_next: bool,
        expected_previous: bool,
        print_json_response: bool = False,
        page_size: Optional[int] = None,
        page: int = 0,
    ) -> Dict:
        URL = reverse("tenantUser")
        if page_size:
            URL = f"{URL}?pageSize={page_size}"
        if page > 0:
            URL = f"{URL}{'&'if page_size else '?'}page={page}"
        response = self.client.get(URL)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.validate_data_in_list_pagination(
            response_dict=response_dict,
            total_count=self.total_count,
            len_list=len_list,
            expected_next=expected_next,
            expected_previous=expected_previous,
            schema_validator=self.validate_tenant_user_in_list,
        )
        return response_dict

    def call_multiples_list(self):
        self.call_tenant_user_list(
            len_list=15,
            expected_next=True,
            expected_previous=False,
        )
        self.call_tenant_user_list(
            len_list=15, expected_next=True, expected_previous=False, page=1
        )
        self.call_tenant_user_list(
            len_list=5,
            expected_next=True,
            expected_previous=True,
            page=2,
            page_size=5,
        )

    def test_tenant_user_list(self):
        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()
        self.call_multiples_list()

        custom_tenant_test_user: CustomTenantTestUser = self.list_tenant_user[0]
        self.login(
            email=custom_tenant_test_user.default_tenant_user.user.email,
            password=custom_tenant_test_user.password,
        )
        self.put_authentication_in_the_header()
        self.call_multiples_list()
