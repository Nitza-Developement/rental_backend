from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase


class TestLogout(AuthAPITestCase):
    def test_logout(self):
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header(access_token="fakeaccesstoken")

        # case: bad access_token, correct refresh_token, result 401
        self.logout(refresh_token=self.refresh_token, unauthorized=True)

        self.put_authentication_in_the_header(access_token=self.access_token)
        # case: bad access_token, bad refresh_token, result 400
        self.logout(refresh_token="fakerefreshtoken", bad_request=True)

        # case: correct access_token, bad refresh_token, result 400
        self.logout(refresh_token="fakerefreshtoken", bad_request=True)
        # case: correct access_token, correct refresh_token, result 200
        self.logout(
            refresh_token=self.refresh_token,
        )
        # case: correct access_token, blacklist refresh_token, result 400
        self.logout(refresh_token=self.refresh_token, bad_request=True)
