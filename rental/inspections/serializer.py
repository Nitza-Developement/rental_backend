from rest_framework import serializers
from rental.inspections.models import Inspection
from rental.forms.models import Form
from rental.models import Vehicle
from rental.forms.serializer import FormSerializer


class InspectionSerializer(serializers.ModelSerializer):
    form = FormSerializer(required=False)

    class Meta:
        model = Inspection
        fields = ("id", "vehicle", "form", "created_at", "field_responses")


class CreateInspectionSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    vehicle = serializers.IntegerField()

    def validate_form(self, value):

        tenant = self.context["request"].user.defaultTenantUser().tenant

        try:
            return Form.objects.get(id=value, tenant=tenant)
        except Form.DoesNotExist:
            raise serializers.ValidationError("Form does not exist")

    def validate_vehicle(self, value):

        tenant = self.context["request"].user.defaultTenantUser().tenant

        try:
            return Vehicle.objects.get(id=value, tenant=tenant)
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle does not exist")
