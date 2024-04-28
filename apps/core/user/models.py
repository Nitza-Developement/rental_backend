from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


def user_name_validator(name: str):
    if name.strip().isspace() or name.strip() == '':
        raise ValidationError(
            message='Name cannot be empty',
            code='invalid')


def get_image_path(user, picture_filename: str):

    if user.id is None:
        raise ValueError('User must have an id to save its profile picture')

    image_extension = picture_filename.split('.')[-1]

    return f'user/{user.id}/image.{image_extension}'


class UserManager(BaseUserManager):
    
    def create_user(self, email, password, role, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        user = self.model(email=email, **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,
                            validators=[user_name_validator])
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def isAdmin(self):
        return self.role == User.ADMIN

    def get_enterprises(self):
        return self.enterprises.filter(is_deleted=False).order_by('name')

    def get_associated_centers(self):
        return self.centers.filter(is_deleted=False).order_by('name')

