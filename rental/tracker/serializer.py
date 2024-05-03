from rest_framework import serializers
from rental.tracker.models import Tracker, TrackerHeartBeatData


class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ['id', 'name', 'vehicle', 'created_date']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                message='Name cannot be empty',
                code='invalid')
        return value


class CreateTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ['name', 'vehicle']
        extra_kwargs = {
            'name': {'required': True},
            'vehicle': {'required': True}
        }

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                message='Name cannot be empty',
                code='invalid')
        return value


class UpdateTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ['name', 'vehicle']
        extra_kwargs = {
            'name': {'required': False},
            'vehicle': {'required': False}
        }

    def validate_name(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                message='Name cannot be empty',
                code='invalid')
        return value


class TrackerHeartBeatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerHeartBeatData
        fields = ['id', 'timestamp', 'latitude', 'longitude', 'tracker']

    def validate_timestamp(self, value):
        if value is None:
            raise serializers.ValidationError(
                message='Timestamp cannot be null',
                code='invalid')
        return value


class CreateTrackerHeartBeatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerHeartBeatData
        fields = ['timestamp', 'latitude', 'longitude', 'tracker']
        extra_kwargs = {
            'timestamp': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
            'tracker': {'required': True}
        }

    def validate_timestamp(self, value):
        if value is None:
            raise serializers.ValidationError(
                message='Timestamp cannot be null',
                code='invalid')
        return value


class UpdateTrackerHeartBeatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerHeartBeatData
        fields = ['timestamp', 'latitude', 'longitude', 'tracker']
        extra_kwargs = {
            'timestamp': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'tracker': {'required': False}
        }

    def validate_timestamp(self, value):
        if value and value is None:
            raise serializers.ValidationError(
                message='Timestamp cannot be null',
                code='invalid')
        return value
