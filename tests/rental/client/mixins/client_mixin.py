
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()


class ClientMixin:
    pass
