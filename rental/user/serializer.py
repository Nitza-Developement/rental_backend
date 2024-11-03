from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from rental.tenantUser.serializer import TenantUserListSerializer
from rental.user.models import User


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "image", "defaultTenantUser", "tenantUsers"]

    defaultTenantUser = serializers.SerializerMethodField()
    tenantUsers = serializers.SerializerMethodField()

    @extend_schema_field(TenantUserListSerializer())
    def get_tenantUsers(self, user: User):
        return TenantUserListSerializer(
            user.tenantUsers, many=True, read_only=True
        ).data

    @extend_schema_field(TenantUserListSerializer())
    def get_defaultTenantUser(self, user: User):
        return TenantUserListSerializer(user.defaultTenantUser(), read_only=True).data


class UpdateUserSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        required=True,
    )
    email = serializers.EmailField(required=False, allow_blank=False, allow_null=True)
    password = serializers.CharField(
        required=False,
        min_length=8,
        max_length=1000,
        allow_blank=False,
        allow_null=True,
    )
    name = serializers.CharField(
        required=False,
        max_length=100,
        allow_blank=False,
        allow_null=True,
        trim_whitespace=True,
    )
    image = serializers.ImageField(required=False, allow_null=True)

    def validate_email(self, new_email):
        if not new_email:
            return new_email

        data: dict = self.initial_data
        user = User.objects.filter(pk=data["id"]).first()
        if user and user.email == new_email:
            return new_email

        existing_user = (
            User.objects.filter(email=new_email)
            .exclude(pk=user.id if user else None)
            .first()
        )

        if existing_user:
            raise serializers.ValidationError(
                detail=f'User with email "{new_email}" already exists', code="unique"
            )

        try:
            validate_email(new_email)
        except ValidationError as e:
            raise serializers.ValidationError(
                detail=f"Invalid email: {e.message}", code="invalid"
            )

        return new_email


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            # "password",
            "image",
        ]
        extra_kwargs = {
            "name": {"write_only": False},
            "email": {"write_only": False},
            # "password": {"write_only": False},
            "image": {"write_only": False},
        }


class ProfilePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True,
        min_length=3,
    )
    new_password = serializers.CharField(
        required=True,
        min_length=3,
    )
    confirm_password = serializers.CharField(
        required=True,
        min_length=3,
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, attrs: dict):
        if self.instance is None:
            raise serializers.ValidationError(
                detail="You must be authenticated to change your password",
                code="not_authenticated",
            )

        user: User = self.instance
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                detail={"old_password": "Old password is incorrect"},
                code="old_password",
            )

        if new_password != confirm_password:
            raise serializers.ValidationError(
                detail={
                    "confirm_password": "New password and confirm password do not match"
                },
                code="confirm_password",
            )

        return attrs

    def save(self, **kwargs):
        if self.instance is None:
            raise serializers.ValidationError(
                detail="You must be authenticated to change your password",
                code="not_authenticated",
            )

        user: User = self.instance
        new_password = self.validated_data.get("new_password")
        user.set_password(new_password)
        user.save()
        return user
