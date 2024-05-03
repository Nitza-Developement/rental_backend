from rest_framework import serializers
from rental.vehicle.models import Vehicle


class VehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'type', 'year', 'make', 'model', 'trim', 'status', 'tracker']


class VehicleCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        required=True,
        choices=Vehicle.TYPE_CHOICES,
        allow_blank=False,
        allow_null=False
    )
    year = serializers.IntegerField(
        required=True,
    )
    make = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False
    )
    model = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=True
    )
    trim = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=False
    )
    vin = serializers.CharField(
        required=True,
        max_length=17,
        allow_blank=False,
        allow_null=False,
    )
    odometer = serializers.IntegerField(
        required=True,
        allow_null=False
    )
    nickname = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False
    )
    spare_tires = serializers.IntegerField(
        required=True,
        allow_null=False
    )
    extra_fields = serializers.JSONField(
        required=False,
        allow_null=True
    )
    status = serializers.ChoiceField(
        required=True,
        choices=Vehicle.STATUS_CHOICES,
        allow_blank=False,
        allow_null=False
    )


class VehicleUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True,
    )
    type = serializers.ChoiceField(
        required=False,
        choices=Vehicle.TYPE_CHOICES,
        allow_blank=False,
        allow_null=True
    )
    year = serializers.IntegerField(
        required=False,
    )
    make = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True
    )
    model = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True
    )
    trim = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True
    )
    vin = serializers.CharField(
        required=False,
        max_length=17,
        allow_blank=False,
        allow_null=True
    )
    odometer = serializers.IntegerField(
        required=False,
        allow_null=False
    )
    nickname = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True
    )
    spare_tires = serializers.IntegerField(
        required=False,
        allow_null=False
    )
    extra_fields = serializers.JSONField(
        required=False,
        allow_null=True
    )
    status = serializers.ChoiceField(
        required=False,
        choices=Vehicle.STATUS_CHOICES,
        allow_blank=False,
        allow_null=True
    )