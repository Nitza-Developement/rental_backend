from django.db.models import Q
from rental.models import User
from rest_framework.exceptions import PermissionDenied
from settings.utils.exceptions import NotFound404APIException


def get_user(user_requesting: User, user_id: str):

    if not user_requesting.isAdmin() and user_requesting.id != user_id:
        raise PermissionDenied()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound404APIException(f"User with id {user_id} not found")

    return user


def create_user(email: str, password: str = 12345678, name: str = "-"):

    new_user = User.objects.create_user(email=email, password=password, name=name)
    new_user.save()
    return new_user


def update_user(user_id: str, email: str, password: str, name: str, image: str = None):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound404APIException(f"User with id {user_id} not found")

    if email:
        user.email = email

    if name:
        user.name = name

    if password:
        user.set_password(password)

    if image:
        user.image = image

    user.full_clean()
    user.save()
    return user


def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()

    except User.DoesNotExist:
        raise NotFound404APIException(f"User with id {user_id} not found")
