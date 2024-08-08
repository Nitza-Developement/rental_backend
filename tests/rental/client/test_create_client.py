from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.client.models import Client
from tests.rental.client.parent_case.client_api_test_case import (
    ClientApiTestCase,
)

User = get_user_model()


class TestCreateClient(ClientApiTestCase):
    def call_create_client(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("client")
        payload = {
            "name": "client",
            "email": "client@example.com",
            "phone_number": "5324351423",
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
