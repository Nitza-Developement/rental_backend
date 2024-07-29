from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from tests.rental.auth.mixins.user_mixin import UserMixin

User = get_user_model()


class AuthAPITestCase(APITestCase, UserMixin):
    def setUp(self):
        self.create_tenant_user_admin()
        self.custom_user = self.create_user()

    def tearDown(self):
        super().tearDown()
        User.objects.all().delete()
