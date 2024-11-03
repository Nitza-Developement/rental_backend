from rest_framework import serializers

from rental.toll.models import TollDue
from rental.vehicle.serializer import VehiclePlateSerializer


class TollDueSerializer(serializers.ModelSerializer):
    createDate = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = TollDue
        fields = [
            "id",
            "amount",
            "plate",
            "contract",
            "stage",
            "invoice",
            "invoiceNumber",
            "createDate",
            "note",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                message="Amount must be greater than zero", code="invalid"
            )
        return value

    def validate_stage(self, value):
        if value not in [TollDue.PAID, TollDue.UNPAID]:
            raise serializers.ValidationError(message="Invalid stage", code="invalid")
        return value


class CreateTollDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollDue
        fields = [
            "amount",
            "plate",
            "contract",
            "stage",
            "invoice",
            "invoiceNumber",
            "note",
        ]
        extra_kwargs = {
            "amount": {"required": True},
            "plate": {"required": True},
            "contract": {"required": True},
            "stage": {"required": True},
            "invoice": {"required": True},
            "invoiceNumber": {"required": True},
            "note": {"required": False},
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                message="Amount must be greater than zero", code="invalid"
            )
        return value

    def validate_stage(self, value):
        if value not in [TollDue.PAID, TollDue.UNPAID]:
            raise serializers.ValidationError(message="Invalid stage", code="invalid")
        return value


class UpdateTollDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollDue
        fields = [
            "amount",
            "plate",
            "contract",
            "stage",
            "invoice",
            "invoiceNumber",
            "note",
        ]
        extra_kwargs = {
            "amount": {"required": False},
            "plate": {"required": False},
            "contract": {"required": False},
            "stage": {"required": False},
            "invoice": {"required": False},
            "invoiceNumber": {"required": False},
            "note": {"required": False},
        }

    def validate_amount(self, value):
        if value and value <= 0:
            raise serializers.ValidationError(
                message="Amount must be greater than zero", code="invalid"
            )
        return value

    def validate_stage(self, value):
        if value and value not in [TollDue.PAID, TollDue.UNPAID]:
            raise serializers.ValidationError(message="Invalid stage", code="invalid")
        return value
