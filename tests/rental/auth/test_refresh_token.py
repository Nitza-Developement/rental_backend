import json
from typing import Optional

from django.urls import reverse
from rest_framework import status

from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase


class TestRefreshToken(AuthAPITestCase):
    def call_refresh_token(
        self,
        refresh_token: Optional[str] = None,
        unauthorized: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("refresh")
        payload = {
            "refresh": self.refresh_token
            if not refresh_token
            else refresh_token
        }
        response = self.client.post(URL, payload)
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
        self.assertEqual(True, "access" in response_dict)
        self.access_token = response_dict["access"]

    def test_refresh_token(self):
        self.login(custom_user=self.custom_user)
        # case: bad refresh_token, result 401
        self.call_refresh_token(
            refresh_token="fakerefreshtoken", unauthorized=True
        )
        last_access_token = self.access_token
        # case: correct refresh_token, result 200
        self.call_refresh_token(refresh_token=self.refresh_token)
        self.assertEqual(True, last_access_token != self.access_token)
        # case: new correct refresh_token, result 200
        self.call_refresh_token(
            refresh_token=self.refresh_token,
        )
