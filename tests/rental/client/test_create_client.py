from typing import Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from rental.client.models import Client
from tests.rental.client.parent_case.client_api_test_case import (
    ClientApiTestCase,
)

fake = Faker()
User = get_user_model()


class TestCreateClient(ClientApiTestCase):
    def call_create_client(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("client")
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

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
        )

    def test_create_client(self):
        initial_amount = Client.objects.count()

        # case not authenticated, response 401
        self.call_create_client(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Client.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_create_client(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Client.objects.count())

        # case correct, response 201
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        response_dict = self.call_create_client(
            print_json_response=False,
            name="client",
            email="client@example.com",
            phone_number="5324351423",
        )
        self.assertEqual(initial_amount + 1, Client.objects.count())
        self.assertEqual(True, "id" in response_dict)
        client_id = response_dict["id"]
        tenant_id = self.custom_staff.user.defaultTenantUser().tenant.id
        self.assertDictEqual(
            response_dict,
            {
                "id": client_id,
                "name": "client",
                "email": "client@example.com",
                "phone_number": "5324351423",
                "tenant": tenant_id,
            },
        )

        # case bad, not unique email, response 400
        self.call_create_client(
            print_json_response=False,
            email="client@example.com",
            bad_request=True,
        )

        # case bad, not unique phone_number, response 400
        self.call_create_client(
            print_json_response=False,
            phone_number="5324351423",
            bad_request=True,
        )
