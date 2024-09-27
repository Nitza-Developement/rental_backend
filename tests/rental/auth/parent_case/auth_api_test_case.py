from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from rental.notes.models import Note
from tests.rental.auth.mixins.user_mixin import UserMixin
from tests.util.api_crud_mixin import ApiCrudMixin

User = get_user_model()


class AuthAPITestCase(APITestCase, UserMixin, ApiCrudMixin):
    def setUp(self):
        self.create_tenant_user_admin()
        self.custom_user = self.create_user()

    def tearDown(self):
        super().tearDown()
        Note.objects.all().delete()
        User.objects.all().delete()
