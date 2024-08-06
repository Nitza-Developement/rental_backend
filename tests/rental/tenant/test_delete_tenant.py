from typing import List

from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.tenant.models import Tenant
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)

User = get_user_model()


class TestDeleteTenant(TenantApiTestCase):
    def setUp(self):
        super().setUp()
        self.list_tenant: List[Tenant] = [
            self.create_tenant() for _ in range(2)
        ]

    def call_tenant_delete(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("tenant-actions", args=[entity_id])
        self.call_delete(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

    def test_delete_tenant(self):
        initial_amount = Tenant.objects.count()

        # case not loguin, response 401
        self.call_tenant_delete(
            entity_id=self.list_tenant[0].id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_tenant_delete(
            entity_id=self.list_tenant[0].id, forbidden=True
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_tenant_delete(
            entity_id=99999,
            not_found=True,
        )
        self.assertEqual(initial_amount, Tenant.objects.count())

        # case correct, response 200
        id_to_delete = self.list_tenant[1].id
        self.assertEqual(True, Tenant.objects.filter(id=id_to_delete).exists())
        self.call_tenant_delete(
            entity_id=id_to_delete,
        )
        self.assertEqual(initial_amount - 1, Tenant.objects.count())
        self.assertEqual(False, Tenant.objects.filter(id=id_to_delete).exists())
