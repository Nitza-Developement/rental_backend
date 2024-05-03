from rental.notes.models import Note
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'contract', 'user', 'subject',
                  'body', 'createdDate', 'remainder', 'file']

    def validate_subject(self, value):
        if value.strip().isspace() or value.strip() == '':
            raise serializers.ValidationError(
                message='Subject cannot be empty',
                code='invalid')
        return value


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['contract', 'user', 'subject', 'body', 'remainder', 'file']
        extra_kwargs = {
            'contract': {'required': True},
            'user': {'required': True},
            'subject': {'required': True},
            'body': {'required': True},
            'remainder': {'required': False},
            'file': {'required': False}
        }

    def validate_subject(self, value):
        if value.strip().isspace() or value.strip() == '':
            raise serializers.ValidationError(
                message='Subject cannot be empty',
                code='invalid')
        return value


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['contract', 'user', 'subject', 'body', 'remainder', 'file']
        extra_kwargs = {
            'contract': {'required': False},
            'user': {'required': False},
            'subject': {'required': False},
            'body': {'required': False},
            'remainder': {'required': False},
            'file': {'required': False}
        }

    def validate_subject(self, value):
        if value and (value.strip().isspace() or value.strip() == ''):
            raise serializers.ValidationError(
                message='Subject cannot be empty',
                code='invalid')
        return value
