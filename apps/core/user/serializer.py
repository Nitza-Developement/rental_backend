from rest_framework import serializers
from apps.core.user.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'image']


class UpdateUserSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        required=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=False,
        allow_null=True
    )
    password = serializers.CharField(
        required=False,
        min_length=8,
        max_length=1000,
        allow_blank=False,
        allow_null=True
    )
    name = serializers.CharField(
        required=False,
        max_length=100,
        allow_blank=False,
        allow_null=True,
        trim_whitespace=True,
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    def validate_email(self, new_email):

        # Do not perform any validation if the email is not provided
        if not new_email:
            return new_email

        data: dict = self.initial_data

        user = User.objects.filter(pk=data['id']).first()

        # Do not perform any validation if the email is equal
        if user and user.email == new_email:
            return new_email

        existing_user = User.objects.filter(email=new_email).exclude(
            pk=user.id if user else None).first()

        if existing_user:
            raise serializers.ValidationError(
                detail=f'User with email "{new_email}" already exists',
                code='unique')

        try:
            validate_email(new_email)
        except ValidationError as e:
            raise serializers.ValidationError(
                detail=f'Invalid email: {e.message}',
                code='invalid')

        return new_email