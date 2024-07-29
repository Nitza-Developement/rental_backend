from rest_framework import serializers

from rental.tenantUser.models import TenantUser


class TenantUserCreateSwaggerRepresentationSerializer(
    serializers.ModelSerializer
):
    email = serializers.EmailField()

    class Meta:
        model = TenantUser
        fields = ["role", "tenant", "is_default", "email"]