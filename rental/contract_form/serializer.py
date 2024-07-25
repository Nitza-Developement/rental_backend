from rest_framework import serializers
from rental.contract_form.models import ContractFormTemplate


class ContractFormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFormTemplate
        fields = "__all__"
