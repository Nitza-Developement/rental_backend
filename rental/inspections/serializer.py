from rest_framework import serializers
from rental.inspections.models import Inspection
from rental.forms.serializer import FormSerializer


class InspectionSerializer(serializers.ModelSerializer):
    form = FormSerializer(required=False)

    class Meta:
        model = Inspection
        fields = ("id", "vehicle", "form", "created_at")
