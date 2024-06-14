from rest_framework import serializers
from rental.forms.models import (
    Form,
    Card,
    Field,
    FieldResponse,
    Inspection,
    CheckOption,
)


class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ("id", "vehicle")


class FieldResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldResponse
        fields = ("inspection", "note", "content", "checked")


class CheckOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOption
        fields = ("id", "name", "type")


class FieldSerializer(serializers.ModelSerializer):

    field_response = FieldResponseSerializer(required=False, many=True)
    check_options = CheckOptionSerializer(required=False, many=True)

    class Meta:
        model = Field
        fields = ("id", "name", "type", "required", "check_options", "field_response")


class CardSerializer(serializers.ModelSerializer):

    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = ("id", "name", "fields")


class FormSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)
    inspections = InspectionSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = ("id", "name", "created_at", "cards", "inspections")
