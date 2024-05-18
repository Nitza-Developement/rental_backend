from rest_framework import serializers
from rental.tenant.models import Tenant
from rental.shared_serializers.serializers import OwnerTenantUserSerializer 


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "email", "name", "isAdmin", "owner"]

    owner = serializers.SerializerMethodField()

    def get_owner(self, tenant:Tenant):
        return OwnerTenantUserSerializer(tenant.owner(), read_only = True).data

    def validate_name(self, value):
        if value.strip().isspace() or value.strip() == "":
            raise serializers.ValidationError(
                message="Name cannot be empty", code="invalid"
            )
        return value


class TenantWithoutAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["email", "name"]


class CreateTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "email",
            "name",
            "isAdmin",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "name": {"required": True},
            "isAdmin": {"required": False},
        }

    def validate_name(self, value):
        if value.strip().isspace() or value.strip() == "":
            raise serializers.ValidationError(
                message="Name cannot be empty", code="invalid"
            )
        return value


class UpdateTenantSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=False, allow_null=True)
    name = serializers.CharField(
        required=False,
        max_length=100,
        allow_blank=False,
        allow_null=True,
        trim_whitespace=True,
    )
    isAdmin = serializers.BooleanField(required=False, allow_null=True)

    def validate_name(self, value):
        if value and (value.strip().isspace() or value.strip() == ""):
            raise serializers.ValidationError(
                message="Name cannot be empty", code="invalid"
            )
        return value
