from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from rental.shared_serializers.serializers import InnerTenantUserSerializer
from rental.tenant.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    tenantUsers = InnerTenantUserSerializer(many=True)

    class Meta:
        model = Tenant
        fields = ["id", "email", "name", "isAdmin", "owner", "tenantUsers"]

    owner = serializers.SerializerMethodField()

    @extend_schema_field(InnerTenantUserSerializer())
    def get_owner(self, tenant: Tenant):
        return InnerTenantUserSerializer(tenant.owner(), read_only=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["tenantUsers"] = InnerTenantUserSerializer(
            instance.tenantUsers.all(), many=True
        ).data

        return representation

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


class UpdateTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "email",
            "name",
            "isAdmin",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "name": {"required": False},
            "isAdmin": {"required": False},
        }

    def validate_name(self, value):
        if value and (value.strip().isspace() or value.strip() == ""):
            raise serializers.ValidationError(
                message="Name cannot be empty", code="invalid"
            )
        return value
