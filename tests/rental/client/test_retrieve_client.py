from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.rental.client.parent_case.client_api_test_case import (
    ClientApiTestCase,
)

User = get_user_model()


class TestRetrieveClient(ClientApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.list_client = [
            self.create_client(user=user),
            self.create_client(user=user),
        ]

    def call_retrieve_client(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        URL = reverse("client-actions", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_client_in_list(
                data=response_dict,
                client_id=entity_id,
            )
        return response_dict

    def test_retrieve_client(self):
        # case not loguin, response 401
        self.call_retrieve_client(
            entity_id=self.list_client[0].id,
            unauthorized=True,
        )

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_retrieve_client(
            entity_id=self.list_client[0].id, forbidden=True
        )

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_retrieve_client(
            entity_id=99999, not_found=True, print_json_response=False
        )

        for entity in self.list_client:
            # case correct, response 200
            self.call_retrieve_client(
                entity_id=entity.id,
            )
