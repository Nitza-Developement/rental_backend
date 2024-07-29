import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase

User = get_user_model()


class TestMe(AuthAPITestCase):
    def call_me(
        self,
        unauthorized: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("user-data")
        response = self.client.get(URL)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def test_me(self):
        self.call_me(unauthorized=True)

        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        response_dict = self.call_me()
        user: User = self.custom_user.user
        user.get_tenantUsers()
        self.assertDictContainsSubset(
            subset={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": user.image,
                "tenantUsers": [],
            },
            dictionary=response_dict,
        )
