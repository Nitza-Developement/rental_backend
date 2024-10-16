from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from rental.client.models import Client


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name", "email", "phone_number"]
        extra_kwargs = {
            "name": {"required": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A client with this email already exists."
            )
        return value

    def validate_phone_number(self, value):
        if Client.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A client with this phone number already exists."
            )
        return value


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "email", "phone_number"]

    def validate_email(self, new_email):
        if not new_email:
            return new_email

        clients_email = Client.objects.filter(email=new_email)
        if self.instance is not None:
            clients_email = clients_email.exclude(id=self.instance.id)

        if clients_email.exists():
            raise serializers.ValidationError(
                detail=f'Client with email "{new_email}" already exists', code="unique"
            )

        try:
            validate_email(new_email)
        except ValidationError as e:
            raise serializers.ValidationError(
                detail=f"Invalid email: {e.message}", code="invalid"
            )

        return new_email

    def validate_phone_number(self, value):
        clients_phone = Client.objects.filter(phone_number=value)
        if self.instance is not None:
            clients_phone = clients_phone.exclude(id=self.instance.id)

        if clients_phone.exists():
            raise serializers.ValidationError(
                "A client with this phone number already exists."
            )
        return value


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "email", "phone_number", "tenant"]
        read_only_fields = ["tenant"]
