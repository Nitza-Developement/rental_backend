from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rental.vehicle.models import Vehicle, VehiclePlate


class VehiclePlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePlate
        fields = ["id", "plate", "assign_date"]


class VehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "vin",
            "nickname",
            "odometer",
            "spare_tires",
            "plate",
            "type",
            "year",
            "make",
            "model",
            "trim",
            "status",
            "tracker",
            "extra_fields",
        ]

    plate = serializers.SerializerMethodField()

    @extend_schema_field(VehiclePlateSerializer())
    def get_plate(self, vehicle: Vehicle):
        return VehiclePlateSerializer(vehicle.active_plate(), read_only=True).data


class VehicleCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        required=False, choices=Vehicle.TYPE_CHOICES, allow_blank=False, allow_null=False
    )
    year = serializers.IntegerField(
        required=False,
    )
    make = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    model = serializers.CharField(required=False, allow_blank=False, allow_null=True)
    trim = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    plate = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    vin = serializers.CharField(
        required=False,
        max_length=17,
        allow_blank=False,
        allow_null=False,
    )
    odometer = serializers.IntegerField(required=False, allow_null=False)
    nickname = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    spare_tires = serializers.IntegerField(required=False, allow_null=False)
    extra_fields = serializers.JSONField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        required=False,
        choices=Vehicle.STATUS_CHOICES,
        allow_blank=False,
        allow_null=False,
    )


class VehicleUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False,
    )
    type = serializers.ChoiceField(
        required=False, choices=Vehicle.TYPE_CHOICES, allow_blank=False, allow_null=False
    )
    year = serializers.IntegerField(
        required=False,
    )
    vin = serializers.CharField(
        required=False,
        max_length=17,
        allow_blank=False,
        allow_null=False,
    )
    make = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    model = serializers.CharField(required=False, allow_blank=False, allow_null=True)
    trim = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    plate = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    odometer = serializers.IntegerField(required=False, allow_null=False)
    nickname = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    spare_tires = serializers.IntegerField(required=False, allow_null=False)
    extra_fields = serializers.JSONField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        required=False,
        choices=Vehicle.STATUS_CHOICES,
        allow_blank=False,
        allow_null=False,
    )

    def validate_vin(self, value):
        if self.instance and self.instance.vin != value:
            if Vehicle.objects.exclude(id=self.instance.id).filter(vin=value).exists():
                raise serializers.ValidationError("A vehicle with this VIN already exists.")
        return value
    
    def validate_plate(self, value):
        try:
            plate_instance = VehiclePlate.objects.get(plate=value)
            if plate_instance and plate_instance.vehicle.id != self.initial_data.get("id"):
                raise serializers.ValidationError("This plate number is already assigned to another vehicle.")
            else:
                return value
        except VehiclePlate.DoesNotExist:
            return value
