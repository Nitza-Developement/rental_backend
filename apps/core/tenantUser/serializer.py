from rest_framework import serializers
from apps.core.tenant.models import TenantUser


class TenantUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['role', 'tenant', 'user', 'is_default']
        read_only_fields = ['tenant', 'user']


class TenantUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['role', 'tenant', 'user', 'is_default']

    def validate_role(self, value):
        if value not in [TenantUser.ADMIN, TenantUser.STAFF, TenantUser.OWNER]:
            raise serializers.ValidationError("Invalid role. Choices are 'Admin', 'Staff', or 'Owner'.")
        return value

    def validate_is_default(self, value):
        if value:
            if TenantUser.objects.filter(tenant=self.context['user'], is_default=True).exists():
                raise serializers.ValidationError("A default tenantUser is already set for this user.")
        return value
    

class TenantUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['role', 'is_default']

    def validate_role(self, value):
        if value not in [TenantUser.ADMIN, TenantUser.STAFF, TenantUser.OWNER]:
            raise serializers.ValidationError("Invalid role. Choices are 'Admin', 'Staff', or 'Owner'.")
        return value

    def validate_is_default(self, value):
        if value:
            if TenantUser.objects.filter(tenant=self.context['tenant'], is_default=True).exists():
                raise serializers.ValidationError("A default tenant user is already set for this tenant.")
        return value

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.is_default = validated_data.get('is_default', instance.is_default)
        instance.save()
        return instance
