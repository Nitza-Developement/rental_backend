import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError


def user_name_validator(name: str):
    if name.strip().isspace() or name.strip() == "":
        raise ValidationError(message="Name cannot be empty", code="invalid")


def get_image_path(user, picture_filename: str):

    if user.id is None:
        raise ValueError("User must have an id to save its profile picture")

    image_extension = picture_filename.split(".")[-1]

    return f"user/{user.id}/image.{image_extension}"


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, validators=[user_name_validator])
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def get_tenantUsers(self):
        return self.tenantUsers.all()

    def __str__(self) -> str:
        return f"{self.email if self.name is None else self.name}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["date_joined"]
