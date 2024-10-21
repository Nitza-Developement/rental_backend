from rest_framework import serializers

from rental.notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(format="%s")
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "contract",
            "user",
            "user_name",
            "subject",
            "body",
            "createdDate",
            "remainder",
            "file",
        ]

    def get_user_name(self, instance: Note):
        if instance.user is None:
            return "UNKNOWN"
        if instance.user.name is None or instance.user.name == "":
            return instance.user.email
        return instance.user.name

    def validate_subject(self, value):
        if value.strip().isspace() or value.strip() == "":
            raise serializers.ValidationError(
                message="Subject cannot be empty", code="invalid"
            )
        return value


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["contract", "user", "subject", "body", "remainder", "file"]
        extra_kwargs = {
            "contract": {"required": True},
            "subject": {"required": True},
            "body": {"required": True},
            "remainder": {"required": False},
            "file": {"required": False},
            "user": {"required": False},
        }

    def validate_subject(self, value: str):
        print(value)
        if value.strip().isspace() or value.strip() == "":
            raise serializers.ValidationError(
                message="Subject cannot be empty", code="invalid"
            )
        return value


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["contract", "user", "subject", "body", "remainder", "file"]
        extra_kwargs = {
            "contract": {"required": False},
            "user": {"required": False},
            "subject": {"required": False},
            "body": {"required": False},
            "remainder": {"required": False},
            "file": {"required": False},
        }

    def validate_subject(self, value):
        if value and (value.strip().isspace() or value.strip() == ""):
            raise serializers.ValidationError(
                message="Subject cannot be empty", code="invalid"
            )
        return value
