from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.tenant.models import Tenant
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)

User = get_user_model()


class TestRetrieveTenant(TenantApiTestCase):
    def setUp(self):
        super().setUp()
        self.list_tenant: List[Tenant] = [
            self.create_tenant() for _ in range(2)
        ]

    def call_tenant_retrieve(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        URL = reverse("tenant-actions", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
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

    def test_retrieve_tenant(self):
        # case not loguin, response 401
        self.call_tenant_retrieve(
            entity_id=self.list_tenant[0].id,
            unauthorized=True,
        )

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_tenant_retrieve(
            entity_id=self.list_tenant[0].id, forbidden=True
        )

        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_tenant_retrieve(
            entity_id=99999,
            not_found=True,
        )

        for tenant in self.list_tenant:
            # case correct, response 200
            self.call_tenant_retrieve(
                entity_id=tenant.id,
            )
