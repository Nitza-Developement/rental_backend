import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rental.tenant.models import Tenant

from ..auth.parent_case.auth_api_test_case import AuthAPITestCase
from .mixins.tenant_user_mixin import TenantUserMixin

User = get_user_model()


class TestTenantUserCreate(AuthAPITestCase, TenantUserMixin):
    def call_tenant_user_create(
        self,
        user: User,
        tenant: Tenant,
        rol: str,
        is_default: bool = True,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenantUser")
        payload = {
            "email": user.email,
            "role": rol,
            "tenant": tenant.id,
            "is_default": is_default,
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
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def test_tenant_user_create(self):
        tenant = self.create_tenant(user=self.custom_user.user)

        # bad authenticated user (not admin), correct data tenant user, response 401
        self.login(custom_user=self.custom_user)
        self.call_tenant_user_create(
            user=self.custom_user.user,
            tenant=tenant,
            rol="Owner",
            is_default=True,
            unauthorized=True,
        )

        # correct authenticated user admin, correct data tenant user, response 201
        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()
        response_dict = self.call_tenant_user_create(
            user=self.custom_user.user,
            tenant=tenant,
            rol="Owner",
            is_default=True,
        )
        user: User = self.custom_user.user
        self.assertEqual(True, "id" in response_dict)
        tenant_user_id = response_dict["id"]
        self.assertDictEqual(
            response_dict,
            {
                "id": tenant_user_id,
                "role": "Owner",
                "tenant": {
                    "id": tenant.id,
                    "email": tenant.email,
                    "name": tenant.name,
                    "isAdmin": tenant.isAdmin,
                    "owner": {
                        "id": tenant_user_id,
                        "role": "Owner",
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "email": user.email,
                            "image": user.image,
                        },
                    },
                    "tenantUsers": [
                        {
                            "id": tenant_user_id,
                            "role": "Owner",
                            "user": {
                                "id": user.id,
                                "name": user.name,
                                "email": user.email,
                                "image": user.image,
                            },
                        }
                    ],
                },
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "image": user.image,
                },
                "is_default": True,
            },
        )

        # correct authenticated user admin, repeated default tenant, response 400
        tenant = self.create_tenant(
            user=self.custom_user.user, email="tenan2@gmail.com"
        )
        self.call_tenant_user_create(
            user=self.custom_user.user,
            tenant=tenant,
            rol="Owner",
            is_default=True,
            bad_request=True,
        )
