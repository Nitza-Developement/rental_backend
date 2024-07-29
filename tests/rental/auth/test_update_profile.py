import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase

User = get_user_model()


class TestUpdateProfile(AuthAPITestCase):
    def call_update_profile(
        self,
        user: User,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("update-profile")
        payload = {
            "id": user.id,
            "email": "edited@example.com",
            "password": "editedpassword",
            "name": "editedname",
        }
        response = self.client.put(URL, payload)
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
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def test_update_profile(self):
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        response_dict = self.call_update_profile(user=self.custom_user.user)
        user: User = self.custom_user.user
        self.assertDictEqual(
            response_dict,
            {
                "id": user.id,
                "email": "edited@example.com",
                "name": "editedname",
                "image": user.image,
            },
        )

        user_2 = self.create_user().user
        self.call_update_profile(
            user=user_2,
            forbidden=True,
        )
