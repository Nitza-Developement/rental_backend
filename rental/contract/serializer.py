from rest_framework import serializers
from rental.notes.serializer import NoteSerializer
from rental.toll.serializer import TollDueSerializer
from rental.contract.models import Contract, StageUpdate
from rental.client.serializer import ClientListSerializer
from rental.vehicle.serializer import VehicleListSerializer
from rental.rentalPlan.serializer import RentalPlanSerializer


class StageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageUpdate
        fields = ["id", "date", "reason", "comments", "stage"]


class StageUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageUpdate
        fields = ["reason", "comments", "stage"]
        extra_kwargs = {
            "reason": {"required": False},
            "comments": {"required": False},
            "stage": {"required": True},
        }


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "tenant",
            "client",
            "vehicle",
            "rental_plan",
            "stages_updates",
            "creation_date",
            "active_date",
            "end_date",
            "stage",
            "notes",
            "toll_dues",
        ]

    stage = serializers.SerializerMethodField()

    def get_stage(self, contract: Contract):
        return StageUpdateCreateSerializer(contract.stages_updates.all()[0]).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["stages_updates"] = StageUpdateSerializer(
            instance.stages_updates.all(), many=True
        ).data
        representation["rental_plan"] = RentalPlanSerializer(instance.rental_plan).data
        representation["client"] = ClientListSerializer(instance.client).data
        representation["vehicle"] = VehicleListSerializer(instance.vehicle).data
        representation["notes"] = NoteSerializer(instance.notes.all(), many=True).data
        representation["toll_dues"] = TollDueSerializer(
            instance.toll_dues.all(), many=True
        ).data

        return representation


class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["client", "vehicle", "rental_plan"]
        extra_kwargs = {
            "client": {"required": True},
            "vehicle": {"required": True},
            "rental_plan": {"required": True},
        }


class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["client", "vehicle", "rental_plan"]
        extra_kwargs = {
            "client": {"required": False},
            "vehicle": {"required": False},
            "rental_plan": {"required": False},
        }
