from attrs import define
from django.contrib.auth import get_user_model

User = get_user_model()


@define
class CustomTestUser:
    user: User
    password: str
