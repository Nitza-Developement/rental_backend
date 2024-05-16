from rest_framework import serializers
from rental.tenantUser.models import TenantUser
from rental.tenant.serializer import TenantSerializer


class OwnerTenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["id", "role", "user"]
        read_only_fields = ["user"]
    

class TenantUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["id", "role", "tenant", "user", "is_default"]
        read_only_fields = ["tenant", "user"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["tenant"] = TenantSerializer(instance.tenant).data

        return representation


class TenantUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["role", "tenant", "is_default"]

    def validate_role(self, value):
        if value not in [TenantUser.ADMIN, TenantUser.STAFF, TenantUser.OWNER]:
            raise serializers.ValidationError(
                "Invalid role. Choices are 'Admin', 'Staff', or 'Owner'."
            )
        return value


class TenantUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["role", "is_default"]

    def validate_role(self, value):
        if value not in [TenantUser.ADMIN, TenantUser.STAFF, TenantUser.OWNER]:
            raise serializers.ValidationError(
                "Invalid role. Choices are 'Admin', 'Staff', or 'Owner'."
            )
        return value
