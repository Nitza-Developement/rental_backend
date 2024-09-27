from auditlog.models import LogEntry
from drf_spectacular.utils import PolymorphicProxySerializer
from rest_framework import serializers

from rental.client.serializer import ClientListSerializer
from rental.contract.models import Contract
from rental.contract.serializer import StageUpdateCreateSerializer, StageUpdateSerializer
from rental.notes.serializer import NoteSerializer
from rental.rentalPlan.serializer import RentalPlanSerializer
from rental.shared_serializers.serializers import UserProfileSerializer
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


class ContractChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    tenant = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    client = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    vehicle = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    rental_plan = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    creation_date = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    active_date = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    notes = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    toll_dues = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    stages_updates = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)

class StageUpdateChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    date = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    reason = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    comments = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    stage = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    contract = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)

class NoteChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    contract = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    user = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    subject = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    body = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    createdDate = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    remainder = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    file = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)

class TollDueChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    amount = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    plate = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    contract = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    stage = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    invoice = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    invoiceNumber = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    createDate = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    note = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)

class RentalPlanChangesHistorySwaggerRepresentationSerializer(serializers.Serializer):
    ID = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    name = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    amount = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    periodicity = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    tenant = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)
    contracts = serializers.ListField(child=serializers.CharField(), min_length=2, max_length=2, required=False)

class AuditlogContractSwaggerRepresentationSerializer(serializers.ModelSerializer):
    actor=UserProfileSerializer()
    changes=PolymorphicProxySerializer(
                                component_name="ChangesAuditlogContractSerializer",
                                serializers=[
                                    ContractChangesHistorySwaggerRepresentationSerializer,
                                    StageUpdateChangesHistorySwaggerRepresentationSerializer,
                                    NoteChangesHistorySwaggerRepresentationSerializer,
                                    TollDueChangesHistorySwaggerRepresentationSerializer,
                                    RentalPlanChangesHistorySwaggerRepresentationSerializer,
                                ],
                                resource_type_field_name="model"
                            )
    model=serializers.ChoiceField(choices=[
        ('contract', 'contract'),
        ('stage_update', 'stage_update'),
        ('note', 'note'),
        ('rental_plan', 'rental_plan'),
        ('toll_due', 'toll_due'),
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

