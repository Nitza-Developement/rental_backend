from rest_framework import serializers

from rental.forms.models import Card
from rental.forms.models import CheckOption
from rental.forms.models import Field
from rental.forms.models import FieldResponse
from rental.forms.models import Form
from settings.settings import MINIO_STORAGE_MEDIA_BUCKET_NAME
from settings.utils.minio_client import minio_client


class FieldResponseSerializer(serializers.ModelSerializer):

    url_file = serializers.SerializerMethodField()

    class Meta:
        model = FieldResponse
        fields = ("note", "content", "check_option_selected", "url_file")

    def get_url_file(self, obj):

        if obj.field.type in (Field.IMAGE, Field.SIGNATURE):

            url = minio_client().presigned_get_object(
                MINIO_STORAGE_MEDIA_BUCKET_NAME, obj.content
            )

            return url

        return None


class CheckOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOption
        fields = ("id", "name", "type")


class FieldSerializer(serializers.ModelSerializer):

    check_options = CheckOptionSerializer(required=False, many=True)
    response = serializers.SerializerMethodField()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Field
        fields = (
            "id",
            "name",
            "type",
            "required",
            "check_options",
            "response",
        )

    def get_response(self, field):

        inspection_id = self.context.get("inspection_id")

        if inspection_id:

            response = FieldResponse.objects.filter(  # pylint: disable=no-member
                inspection__id=inspection_id,
                field__id=field.id,
            ).first()

            if not response:
                return None

            return FieldResponseSerializer(response).data

        return None


class CardSerializer(serializers.ModelSerializer):

    fields = FieldSerializer(many=True)

    class Meta:
        model = Card
        fields = ("id", "name", "fields")


class FormSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = ("id", "name", "created_at", "cards", "inspections")
        extra_kwargs = {"inspections": {"required": False}}
