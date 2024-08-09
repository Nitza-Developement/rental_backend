from rest_framework import serializers

from rental.client.serializer import ClientListSerializer
from rental.contract.models import Contract
from rental.contract.serializer import StageUpdateCreateSerializer, StageUpdateSerializer
from rental.notes.serializer import NoteSerializer
from rental.rentalPlan.serializer import RentalPlanSerializer
from rental.toll.serializer import TollDueSerializer
from rental.vehicle.serializer import VehicleListSerializer


class ContractSwaggerRepresentationSerializer(serializers.ModelSerializer):
    stage=StageUpdateCreateSerializer()
    stages_updates=StageUpdateSerializer(many=True)
    rental_plan=RentalPlanSerializer()
    client=ClientListSerializer()
    vehicle=VehicleListSerializer()
    notes=NoteSerializer(many=True)
    toll_dues=TollDueSerializer(many=True)
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