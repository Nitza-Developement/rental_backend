from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.tenant.models import Tenant

from ..auth.parent_case.auth_api_test_case import AuthAPITestCase

User = get_user_model()


class TestCreateTenant(AuthAPITestCase):
    def call_create_tenant(
        self,
        email: str,
        name: str,
        is_default: bool = True,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenant")
        payload = {
            "email": email,
            "name": name,
            "is_default": is_default,
        }

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
        )

    def test_create_tenant(self):
        initial_amount = Tenant.objects.count()

        # case not authenticated, response 401
        self.call_create_tenant(
            email="testtenant@gmail.com",
            name="testtenant",
            is_default=False,
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_create_tenant(
            email="testtenant@gmail.com",
            name="testtenant",
            is_default=False,
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case correct, response 201
        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()
        response_dict = self.call_create_tenant(
            email="testtenant@gmail.com",
            name="testtenant",
            is_default=False,
            print_json_response=False,
        )
        self.assertEqual(initial_amount + 1, Tenant.objects.count())
        self.assertEqual(True, "id" in response_dict)
        tenant_id = response_dict["id"]
        self.assertDictEqual(
            response_dict,
            {
                "id": tenant_id,
                "email": "testtenant@gmail.com",
                "name": "testtenant",
                "isAdmin": False,
                "owner": {
                    "role": None,
                    "user": {"name": "", "email": "", "image": None},
                },
                "tenantUsers": [],
            },
        )

        # case email not unique
        self.call_create_tenant(
            email="testtenant@gmail.com",
            name="testtenant",
            is_default=False,
            bad_request=True,
        )
