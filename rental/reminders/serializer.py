from rest_framework import serializers

from rental.reminders.models import Reminder
from rental.tenantUser.models import TenantUser
from rental.user.models import User


class ReminderSerializer(serializers.ModelSerializer):
    remainder = serializers.DateTimeField(
        required=False,
        allow_null=True,
        format="%Y-%m-%d",
    )
    created_at = serializers.DateTimeField(format="%s", read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)

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
            # Meta data
            "created_at",
            "created_by",
            "created_by_name",
            # Links
            "contract",
            "vehicle",
            "client",
            "toll_due",
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
