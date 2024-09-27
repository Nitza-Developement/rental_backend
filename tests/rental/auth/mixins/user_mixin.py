import json
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

from rental.models import Tenant, TenantUser
from tests.rental.auth.utils.custom_test_user import CustomTestUser

faker = Faker()

User = get_user_model()

T = TypeVar("T")


class UserMixin:
    def create_tenant_user_admin(
        self, tenant: Optional[Tenant] = None
    ) -> TenantUser:
        self.admin_email = "admin@gmail.com"
        self.admin_password = "123"
        self.admin_user = User.objects.create_user(
            email=self.admin_email, password=self.admin_password
        )
        if not tenant:
            tenant = Tenant.objects.create(
                email=self.admin_email, name="tenant_admin", isAdmin=True
            )
        tenant_user = TenantUser.objects.create(
            role=TenantUser.ADMIN,
            tenant=tenant,
            user=self.admin_user,
            is_default=True,
        )
        return tenant_user

    def create_user(self) -> CustomTestUser:
        password = faker.password(length=8)
        user = User.objects.create_user(email=faker.email(), password=password)
        return CustomTestUser(user=user, password=password)

    def login(
        self,
        custom_user: Optional[CustomTestUser] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        unauthorized: bool = False,
    ):
        URL = reverse("login")
        payload = {
            "password": custom_user.password if custom_user else password,
            "email": custom_user.user.email if custom_user else email,
        }
        response = self.client.post(URL, payload)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.assertEqual(True, "access" in response_dict)
        self.assertEqual(True, "refresh" in response_dict)
        self.access_token = response_dict["access"]
        self.refresh_token = response_dict["refresh"]

    def logout(
        self,
        refresh_token: Optional[str] = None,
        unauthorized: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("logout")
        payload = {
            "refreshToken": self.refresh_token
            if not refresh_token
            else refresh_token
        }
        response = self.client.post(URL, payload)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def put_authentication_in_the_header(
        self, access_token: Optional[str] = None
    ):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token if not access_token else access_token}"
        )

    def clear_authentication_in_the_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    def assertKey(
        self,
        response_dict: Dict[str, Any],
        key: str,
        expected: Optional[T] = None,
        expected_any: Optional[List[T]] = None,
        expected_type: Optional[T] = None,
        expected_none: bool = False,
        expected_in_list_of_type: Optional[List[Type]] = None,
        expected_dict: Optional[Dict[str, Any]] = None,
    ) -> T:
        if key not in response_dict:
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
            print(f"key {key}")

        self.assertEqual(True, key in response_dict)
        value: T = response_dict[key]
        if expected is not None:
            self.assertEqual(value, expected)
        elif expected_any is not None:
            self.assertEqual(True, value in expected_any)
        elif expected_in_list_of_type is not None:
            self.assertEqual(True, isinstance(value, list))
            self.assertEqual(len(expected_in_list_of_type), len(value))
            for i, element in enumerate(value):
                self.assertEqual(
                    True, isinstance(element, expected_in_list_of_type[i])
                )
        elif expected_type:
            self.assertEqual(True, isinstance(value, expected_type))
        elif expected_dict:
            self.assertEqual(True, isinstance(value, dict))
            self.assertDictEqual(value, expected_dict)
        else:
            self.assertEqual(expected_none, value is None)
        return value

    def validate_data_in_list_pagination(
        self,
        response_dict: Dict,
        total_count: int,
        len_list: int,
        expected_next: bool,
        expected_previous: bool,
        schema_validator: Callable[[Dict], None],
    ):
        self.assertKey(
            response_dict=response_dict, key="count", expected=total_count
        )
        self.assertKey(
            response_dict=response_dict,
            key="next",
            expected_none=not expected_next,
        )
        self.assertKey(
            response_dict=response_dict,
            key="previous",
            expected_none=not expected_previous,
        )
        self.assertEqual(True, "results" in response_dict)
        results = response_dict["results"]
        self.assertIsInstance(results, list)
        self.assertEqual(len_list, len(results))
        for result in results:
            self.assertIsInstance(result, dict)
            schema_validator(result)
