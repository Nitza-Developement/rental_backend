from rest_framework import serializers

from rental.client.serializer import ClientListSerializer
from rental.contract.serializer import ContractSerializer
from rental.reminders.models import Reminder
from rental.tenantUser.models import TenantUser
from rental.toll.serializer import TollDueSerializer
from rental.user.models import User
from rental.vehicle.serializer import VehicleListSerializer


class SimpleReminderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%s", read_only=True)

    class Meta:
        model = Reminder
        fields = [
            "id",
            "status",
            "important",
            "title",
            "remainder",
            "created_at",
        ]


class ReminderSerializer(serializers.ModelSerializer):
    remainder = serializers.DateTimeField(
        required=False,
        allow_null=True,
        format="%Y-%m-%d",
    )
    created_at = serializers.DateTimeField(format="%s", read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)

    contract_link = serializers.SerializerMethodField(read_only=True)
    vehicle_link = serializers.SerializerMethodField(read_only=True)
    client_link = serializers.SerializerMethodField(read_only=True)
    toll_due_link = serializers.SerializerMethodField(read_only=True)
    reminder_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reminder
        fields = [
            "id",
            # Note fields
            "status",
            "important",
            "title",
            "content",
            "remainder",
            "file",
            "file_name",
            # Meta data
            "created_at",
            "created_by",
            "created_by_name",
            # Links
            "contract",
            "contract_link",
            "vehicle",
            "vehicle_link",
            "client",
            "client_link",
            "toll_due",
            "toll_due_link",
            "reminder",
            "reminder_link",
        ]
        extra_kwargs = {
            "created_by": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def get_created_by_name(self, instance: Reminder):
        if not instance or not instance.created_by:
            return "UNKNOWN"

        tenant_user: TenantUser = instance.created_by
        if not tenant_user.user:
            return tenant_user.role

        user: User = tenant_user.user
        if user.name:
            return user.name
        if user.email:
            return user.email
        return "UNKNOWN"

    def get_file_name(self, instance: Reminder):
        if not instance or not instance.file:
            return None

        return instance.file.name

    def get_contract_link(self, instance: Reminder):
        if not instance or not instance.contract:
            return None

        return ContractSerializer(instance.contract).data

    def get_vehicle_link(self, instance: Reminder):
        if not instance or not instance.vehicle:
            return None

        return VehicleListSerializer(instance.vehicle).data

    def get_client_link(self, instance: Reminder):
        if not instance or not instance.client:
            return None

        return ClientListSerializer(instance.client).data

    def get_toll_due_link(self, instance: Reminder):
        if not instance or not instance.toll_due:
            return None

        return TollDueSerializer(instance.toll_due).data

    def get_reminder_link(self, instance: Reminder):
        if not instance or not instance.reminder:
            return None

        return SimpleReminderSerializer(instance.reminder).data

    def validate_title(self, value):
        if value is None or len(value) < 1:
            raise serializers.ValidationError("Title is required")

        titles = Reminder.objects.filter(
            title=value,
            created_by=self.context["tenant_user"],
        )
        if self.instance:
            titles = titles.exclude(id=self.instance.id)
        if titles.exists():
            raise serializers.ValidationError("Title already exists")

        return value

    def save(self, **kwargs):
        if self.instance is None:
            kwargs["created_by"] = self.context["tenant_user"]
        return super().save(**kwargs)
