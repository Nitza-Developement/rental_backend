from rest_framework import serializers
from apps.core.client.models import Client


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'tenant']

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A client with this email already exists.")
        return value

    def validate_phone_number(self, value):
        if Client.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A client with this phone number already exists.")
        return value


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number']

    def validate_email(self, value):
        if Client.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(
                "A client with this email already exists.")
        return value

    def validate_phone_number(self, value):
        if Client.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(
                "A client with this phone number already exists.")
        return value


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'tenant']
        read_only_fields = ['tenant']
