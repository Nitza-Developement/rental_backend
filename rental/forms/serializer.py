from rest_framework import serializers


from rental.forms.models import Form, Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("name",)


class FormSerializer(serializers.ModelSerializer):

    cards = CardSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = ("id", "name", "created_at", "cards")
