from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer
from rest_framework import serializers
from auditlog.models import LogEntry

from rental.shared_serializers.serializers import UserProfileSerializer


class VehicleChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    type = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    year = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    make = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    model = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    trim = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    plate = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    vin = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    odometer = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    nickname = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    spare_tires = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    status = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)

class VehiclePlateChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    plate = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    vehicle = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    is_active = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    toll_dues = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    assign_date = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)

class VehiclePictureChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    image = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    vehicle = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)
    pinned = serializers.ListField(child=serializers.CharField(),min_length=2,max_length=2,required=False)

class AuditlogVehicleSwaggerRepresentationSerializer(serializers.ModelSerializer):
    actor=UserProfileSerializer()
    changes=PolymorphicProxySerializer(
                                component_name="ChangesAuditlogVehicleSerializer",
                                serializers=[
                                    VehicleChangesHistorySwaggerRepresentationSerializer,
                                    VehiclePlateChangesHistorySwaggerRepresentationSerializer,
                                    VehiclePictureChangesHistorySwaggerRepresentationSerializer,
                                ],
                                resource_type_field_name="model"
                            )
    model=serializers.ChoiceField(choices=[
        ('vehicle','vehicle'),('plate','plate'),('picture','picture'),
    ])
    class Meta:
        model = LogEntry
        fields = [
            'action',
            'changes',
            'timestamp',
            'actor',
            'model',
        ]

