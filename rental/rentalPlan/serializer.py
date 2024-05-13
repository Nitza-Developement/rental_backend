from rest_framework import serializers
from rental.rentalPlan.models import RentalPlan


class RentalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalPlan
        fields = ['id', 'name', 'amount', 'periodicity']

    def validate_name(self, value):
        if value.strip().isspace() or value.strip() == '':
            raise serializers.ValidationError(
                message='Name cannot be empty',
                code='invalid')
        return value


class CreateRentalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalPlan
        fields = [
            'name',
            'amount',
            'periodicity',
        ]
        extra_kwargs = {
            'name': {
                'required': True,
                'allow_null': False,
                'unique': True
            },
            'amount': {
                'required': True,
                'allow_null': False
            },
            'periodicity': {
                'required': True,
                'allow_null': False
            }
        }

    def validate_name(self, value):
        if value.strip().isspace() or value.strip() == '':
            raise serializers.ValidationError(
                message='Name cannot be empty',
                code='invalid')
        return value


class UpdateRentalPlanSerializer(serializers.Serializer):
    class Meta:
        model = RentalPlan
        fields = [
            'name',
            'amount',
            'periodicity',
        ]
        extra_kwargs = {
            'name': {
                'required': False,
                'allow_null': False,
                'unique': True
            },
            'amount': {
                'required': False,
                'allow_null': False
            },
            'periodicity': {
                'required': False,
                'allow_null': False
            }
        }