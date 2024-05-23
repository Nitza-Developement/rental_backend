from rest_framework import serializers
from rental.contract.models import Contract, StageUpdate


class StageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageUpdate
        fields = ["id", "date", "reason", "comments", "stage"]


class StageUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageUpdate
        fields = ["date", "reason", "comments", "stage"]
        extra_kwargs = {
            "date": {"required": False},
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
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["stages_updates"] = StageUpdateSerializer(
            instance.stages_updates.all(), many=True
        ).data

        return representation


class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["tenant", "client", "vehicle", "rental_plan"]
        extra_kwargs = {
            "tenant": {"required": True},
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
