from rest_framework import serializers
from django.core.validators import validate_email
from rental.inspections.models import Inspection
from rental.forms.models import Form, Field
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


class CreateInspectionResponseSerializer(serializers.Serializer):
    inspection = serializers.IntegerField()
    response = serializers.JSONField()

    def validate_inspection(self, value):

        tenant = self.context["request"].user.defaultTenantUser().tenant

        try:
            Inspection.objects.get(id=value, tenant=tenant)
        except Inspection.DoesNotExist:
            raise serializers.ValidationError("Inspection does not exist")

        return value

    def validate_response(self, value: dict):

        for key in value.keys():

            field = self.check_field(key)
            self.check_field_value(field, value[key])

    def check_field_value(self, field: Field, value):

        if field.type in (Field.TEXT, Field.DATE, Field.TIME, Field.PHONE):
            if not isinstance(value, str):
                raise serializers.ValidationError(f"Field {field.id} must be a string")

        elif field.type in (Field.NUMBER, Field.SINGLE_CHECK):
            if not isinstance(value, int) and not isinstance(value, float):
                raise serializers.ValidationError(f"Field {field.id} must be a number")

        elif field.type == Field.EMAIL:
            try:
                validate_email(value)
            except:
                raise serializers.ValidationError(
                    f"Field {field.id} must be a valid email"
                )

        elif field.type == Field.IMAGE:
            print(value)


