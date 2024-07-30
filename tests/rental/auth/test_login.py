from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase


class TestLoguin(AuthAPITestCase):
    def test_login(self):
        self.login(
            email="fakeemail@gmail.com",
            password="fakepassword",
            unauthorized=True,
        )
        self.login(
            email=self.custom_user.user.email,
            password="fakepassword",
            unauthorized=True,
        )
        self.login(custom_user=self.custom_user)
