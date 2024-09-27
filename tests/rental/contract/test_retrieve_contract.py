from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.rental.contract.parent_case.contract_api_test_case import (
    ContractApiTestCase,
)

User = get_user_model()


class TestRetrieveContract(ContractApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.list_contract = [
            self.create_contract(
                user=user,
                client=self.create_client(user=user),
                vehicle=self.create_vehicle(user=user),
                rental_plan=self.create_rental_plan(user=user),
            )
            for _ in range(2)
        ]

    def call_retrieve_contract(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        URL = reverse("contract-actions", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_contract_in_list(
                data=response_dict,
                contract_id=entity_id,
            )
        return response_dict

    def test_retrieve_contract(self):
        # case not loguin, response 401
        self.call_retrieve_contract(
            entity_id=self.list_contract[0].id,
            unauthorized=True,
        )

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_retrieve_contract(
            entity_id=self.list_contract[0].id, forbidden=True
        )

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_retrieve_contract(
            entity_id=99999, not_found=True, print_json_response=False
        )

        for entity in self.list_contract:
            # case correct, response 200
            self.call_retrieve_contract(
                entity_id=entity.id,
            )
