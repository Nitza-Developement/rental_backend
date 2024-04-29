from rest_framework import serializers
from rental.client.models import Client
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'tenant']
        extra_kwargs = {
            'name': {
                'required': True
            },
            'email': {
                'required': True
            },
            'tenant': {
                'required': False
            }
        }

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
        fields = ['id', 'name', 'email', 'phone_number']

    def validate_email(self, new_email):
        if not new_email:
            return new_email

        data: dict = self.initial_data

        client = Client.objects.filter(pk=data['id']).first()

        if client and client.email == new_email:
            return new_email

        existing_client = Client.objects.filter(email=new_email).exclude(
            pk=client.id if client else None).first()

        if existing_client:
            raise serializers.ValidationError(
                detail=f'Client with email "{new_email}" already exists',
                code='unique')

        try:
            validate_email(new_email)
        except ValidationError as e:
            raise serializers.ValidationError(
                detail=f'Invalid email: {e.message}',
                code='invalid')

        return new_email

    def validate_phone_number(self, value):
        data: dict = self.initial_data
        client = Client.objects.filter(pk=data['id']).first()
        if Client.objects.filter(phone_number=value).exclude(pk=client.id if client else None).exists():
            raise serializers.ValidationError(
                "A client with this phone number already exists.")
        return value


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone_number', 'tenant']
        read_only_fields = ['tenant']
