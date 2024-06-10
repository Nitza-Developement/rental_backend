from rest_framework import serializers
from rental.forms.models import Form, Card, Field, FieldResponse, Inspection


class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ("id", "vehicle")
        read_only_fields = ["id"]


class FieldResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldResponse
        fields = ("inspection", "note", "content", "checked")


class FieldSerializer(serializers.ModelSerializer):

    field_response = FieldResponseSerializer(required=False, many=True)

    class Meta:
        model = Field
        fields = ("id", "name", "type", "field_response")
        read_only_fields = ["id"]


class CardSerializer(serializers.ModelSerializer):

    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = ("name", "fields")


class FormSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = ("id", "name", "created_at", "cards")
