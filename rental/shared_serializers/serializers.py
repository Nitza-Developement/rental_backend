from rest_framework import serializers
from rental.models import TenantUser, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "image"]


class OwnerTenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["id", "role", "user"]
        read_only_fields = ["user"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['user'] = UserProfileSerializer(instance.user).data

        return representation