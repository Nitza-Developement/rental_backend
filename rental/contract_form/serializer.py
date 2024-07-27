from rest_framework import serializers
from rental.contract_form.models import ContractFormTemplate


class ContractFormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFormTemplate
        fields = ("id", "name", "template", "user", "tenant", "created_at")
        extra_kwargs = {
            "template": {"required": False},
            "user": {"required": False},
            "tenant": {"required": False},
        }


class UpdateContractFormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFormTemplate
        fields = ("name", "template")
        extra_kwargs = {
            "template": {"required": False},
            "name": {"required": False},
        }
