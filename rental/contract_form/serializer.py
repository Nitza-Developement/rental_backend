from rest_framework import serializers
from rental.contract_form.models import ContractFormTemplate, ContractForm


class ContractFormTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractFormTemplate
        fields = ("id", "name", "template", "user", "tenant", "created_at", "contracts")
        extra_kwargs = {
            "template": {"required": False},
            "user": {"required": False},
            "tenant": {"required": False},
            "contracts": {"required": False},
        }


class UpdateContractFormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFormTemplate
        fields = ("name", "template")
        extra_kwargs = {
            "template": {"required": False},
            "name": {"required": False},
        }


class CloneContractFormTemplateSerializer(serializers.Serializer):

    form_id = serializers.IntegerField()

    def validate_form_id(self, value):

        tenant = self.context.get("tenant")
        try:
            self.instance = ContractFormTemplate.objects.get(id=value, tenant=tenant)
        except ContractFormTemplate.DoesNotExist:
            raise serializers.ValidationError("Template does not exist")

        return value


class ContractFormSerializer(serializers.ModelSerializer):
    template = ContractFormTemplateSerializer()

    class Meta:
        model = ContractForm
        fields = ("id", "name", "template", "user", "tenant", "created_at")


class CreateContractFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractForm
        fields = ("name", "template")

    def validate_template(self, value):

        if value.tenant != self.context.get("tenant"):
            raise serializers.ValidationError("Template does not exist")

        return value
