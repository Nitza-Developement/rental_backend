from rest_framework import serializers

from rental.contract_form.models import ContractForm
from rental.contract_form.models import ContractFormField
from rental.contract_form.models import ContractFormFieldResponse
from rental.contract_form.models import ContractFormTemplate
from settings.settings import MINIO_STORAGE_MEDIA_BUCKET_NAME
from settings.utils.minio_client import minio_client


class ContractFormFieldResponseSerializer(serializers.ModelSerializer):
    url_file = serializers.SerializerMethodField()

    class Meta:
        model = ContractFormFieldResponse
        fields = ("id", "content", "url_file")

    def get_url_file(self, obj):

        if obj.field.type == ContractFormField.SIGNATURE:

            url = minio_client().presigned_get_object(
                MINIO_STORAGE_MEDIA_BUCKET_NAME, obj.content
            )

            return url

        return None


class ContractFormFieldSerializer(serializers.ModelSerializer):

    response = serializers.SerializerMethodField()

    class Meta:
        model = ContractFormField
        fields = ("id", "type", "placeholder", "required", "response")

    def get_response(self, field):

        contract_form_id = self.context.get("contract_form_id")
        if contract_form_id:

            response = ContractFormFieldResponse.objects.filter(
                form_id=contract_form_id,
                field_id=field.id,
            ).first()

            if not response:
                return None

            return ContractFormFieldResponseSerializer(response).data

        return None


class ContractFormTemplateSerializer(serializers.ModelSerializer):
    fields = ContractFormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = ContractFormTemplate
        fields = (
            "id",
            "name",
            "template",
            "user",
            "tenant",
            "created_at",
            "contracts",
            "fields",
        )
        extra_kwargs = {
            "id": {"required": False},
            "template": {"required": False},
            "user": {"required": False},
            "tenant": {"required": False},
            "contracts": {"required": False},
            "created_at": {"read_only": True},
        }


class UpdateContractFormTemplateSerializer(serializers.ModelSerializer):

    fields = ContractFormFieldSerializer(many=True, required=False)

    class Meta:
        model = ContractFormTemplate
        fields = ("name", "template", "fields")
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
    completed = serializers.SerializerMethodField()

    class Meta:
        model = ContractForm
        fields = (
            "id",
            "name",
            "template",
            "user",
            "tenant",
            "created_at",
            "completed",
        )

    def get_completed(self, contract_form):
        return ContractFormFieldResponse.objects.filter(form=contract_form).exists()


class CreateContractFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractForm
        fields = ("name", "template")

    def validate_template(self, value):

        if value.tenant != self.context.get("tenant"):
            raise serializers.ValidationError("Template does not exist")

        return value
