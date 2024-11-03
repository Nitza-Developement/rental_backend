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

            response = FieldResponse.objects.filter(
                inspection__id=inspection_id,
                field__id=field.id,
            ).first()

            if not response:
                return None

            return FieldResponseSerializer(response).data

        return None

    def validate_check_options(self, check_options: list[dict]):
        # Created check_options
        self.check_options_id = [
            check_option["id"] for check_option in check_options if "id" in check_option
        ]
        check_options_instances = CheckOption.objects.filter(
            id__in=self.check_options_id
        )

        # Map check_options by id
        check_options_map = {}
        for check_option in check_options_instances:
            check_options_map[check_option.id] = check_option

        # Create all check_options serializers
        self.check_options_ser = [
            CheckOptionSerializer(
                (
                    check_options_map[check_option["id"]]
                    if "id" in check_option and check_option["id"] in check_options_map
                    else None
                ),
                data=check_option,
            )
            for check_option in check_options
        ]

        # Validate them
        for cs in self.check_options_ser:
            cs.is_valid(raise_exception=True)
        return check_options

    def save(self, **kwargs):
        # Save field
        self.validated_data.pop("check_options", [])
        instance = super().save(**kwargs)
        # Remove unused old check_options
        CheckOption.objects.filter(field=instance).exclude(
            id__in=self.check_options_id
        ).delete()
        # Update or create check_options
        for cs in self.check_options_ser:
            cs.save(field=instance)
        return instance


class CardSerializer(serializers.ModelSerializer):

    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = ("id", "name", "fields")

    def validate_fields(self, fields: list[dict]):
        # Created cards
        self.fields_id = [field["id"] for field in fields if "id" in field]
        fields_instances = Field.objects.filter(id__in=self.fields_id)

        # Map cards by id
        fields_map = {}
        for field in fields_instances:
            fields_map[field.id] = field

        # Create all cards serializers
        self.fields_ser = [
            FieldSerializer(
                (
                    fields_map[field["id"]]
                    if "id" in field and field["id"] in fields_map
                    else None
                ),
                data=field,
            )
            for field in fields
        ]

        for fs in self.fields_ser:
            fs.is_valid(raise_exception=True)
        return fields

    def save(self, **kwargs):
        # Save card
        self.validated_data.pop("fields", [])
        instance = super().save(**kwargs)
        # Remove unused old fields
        Field.objects.filter(card=instance).exclude(id__in=self.fields_id).delete()
        # Update or create fields
        for fs in self.fields_ser:
            fs.save(card=instance)
        return instance


class FormSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = ("id", "name", "created_at", "cards", "inspections")
        extra_kwargs = {"inspections": {"required": False}}

    def validate_cards(self, cards):
        # Created cards
        self.cards_id = [card["id"] for card in cards if "id" in card]
        cards_instances = Card.objects.filter(id__in=self.cards_id)

        # Map cards by id
        cards_map = {}
        for card in cards_instances:
            cards_map[card.id] = card

        # Create all cards serializers
        self.cards_ser = [
            CardSerializer(
                (
                    cards_map[card["id"]]
                    if "id" in card and card["id"] in cards_map
                    else None
                ),
                data=card,
            )
            for card in cards
        ]
        # Validate them
        for cs in self.cards_ser:
            cs.is_valid(raise_exception=True)
        return cards

    def save(self, **kwargs):
        # Save form
        self.validated_data.pop("cards", [])
        instance = super().save(**kwargs)
        # Remove unused old cards
        Card.objects.filter(form=instance).exclude(id__in=self.cards_id).delete()
        # Update or create cards
        for cs in self.cards_ser:
            cs.save(form=instance)
        return instance
