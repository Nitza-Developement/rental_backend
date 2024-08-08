from typing import Optional

from django.urls import reverse
from faker import Faker

from rental.client.models import Client
from tests.rental.client.parent_case.client_api_test_case import (
    ClientApiTestCase,
)

fake = Faker()


class TestUpdateClient(ClientApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.list_client = [
            self.create_client(user=user),
            self.create_client(user=user),
        ]

    def call_update_client(
        self,
        entity_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("client-actions", args=[entity_id])
        # print(URL)
        if not name:
            name = fake.first_name()
        if not email:
            email = (fake.email(),)
        if not phone_number:
            phone_number = (fake.phone_number(),)
        payload = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
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
            self.validate_client_in_list(
                data=response_dict,
                client_id=entity_id,
            )
        return response_dict

    def test_update_client(self):
        initial_amount_client = Client.objects.count()
        client = self.list_client[0]

        # case not authenticated, response 401
        self.call_update_client(
            entity_id=client.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_client, Client.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_update_client(
            entity_id=client.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_client, Client.objects.count())

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_client(
            entity_id=999999, not_found=True, print_json_response=False
        )
        self.assertEqual(initial_amount_client, Client.objects.count())

        # case correct, response 200
        self.call_update_client(
            entity_id=client.id,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_client, Client.objects.count())

        # case bad, not unique email, response 400
        other_client = self.list_client[1]
        self.call_update_client(
            entity_id=client.id,
            email=other_client.email,
            bad_request=True,
        )
        self.assertEqual(initial_amount_client, Client.objects.count())

        # case bad, not unique phone_number, response 400
        other_client = self.list_client[1]
        self.call_update_client(
            entity_id=client.id,
            phone_number=other_client.phone_number,
            bad_request=True,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_client, Client.objects.count())
