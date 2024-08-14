from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.tenant.models import Tenant
from rental.tenantUser.models import TenantUser
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)

User = get_user_model()


class TestUpdateTenant(TenantApiTestCase):
    def setUp(self):
        super().setUp()
        self.custom_owner: CustomTenantTestUser = self.create_tenant_user()
        self.tenant_user_owner: TenantUser = (
            self.custom_owner.default_tenant_user
        )
        self.tenant = self.create_tenant(
            user=self.custom_user.user, email=self.custom_user.user.email
        )

    def call_update_tenant(
        self,
        entity_id: int,
        email: str,
        name: str,
        isAdmin: bool,
        ownerId: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenant-actions", args=[entity_id])
        payload = {
            "id": entity_id,
            "email": email,
            "name": name,
            "isAdmin": isAdmin,
            "ownerId": ownerId,
        }
        response_dict = self.call_update(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_tenant_in_list(
                data=response_dict,
                tenant_id=entity_id,
                # tenant_user_owner=TenantUser.objects.get(id=ownerId)
            )
        return response_dict

    def test_update_tenant(self):
        initial_amount = Tenant.objects.count()

        # case not authenticated, response 401
        self.call_update_tenant(
            entity_id=self.tenant.id,
            email="testtenant@gmail.com",
            name="testtenant",
            isAdmin=False,
            ownerId=self.tenant_user_owner.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case bad authenticated user (not admin), response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_update_tenant(
            entity_id=self.tenant.id,
            email="testtenant@gmail.com",
            name="testtenant",
            isAdmin=False,
            ownerId=self.tenant_user_owner.id,
            forbidden=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_tenant(
            entity_id=999999,
            email="testtenant@gmail.com",
            name="testtenant",
            isAdmin=False,
            ownerId=self.tenant_user_owner.id,
            not_found=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case not found owner, response 404
        self.call_update_tenant(
            entity_id=self.tenant.id,
            email="testtenant@gmail.com",
            name="testtenant",
            isAdmin=False,
            ownerId=99999,
            not_found=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case correct, response 200
        self.call_update_tenant(
            entity_id=self.tenant.id,
            email="testtenant@gmail.com",
            name="testtenant",
            isAdmin=False,
            ownerId=self.tenant_user_owner.id,
            print_json_response=False,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())
