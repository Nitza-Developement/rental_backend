from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rental.reminders.models import Reminder
from rental.reminders.serializer import ReminderSerializer
from rental.tenantUser.models import TenantUser


class ReminderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    def get_serializer_context(self):
        tenant: TenantUser = self.request.user.defaultTenantUser()
        ctx = super().get_serializer_context()
        ctx["tenant_user"] = tenant
        return ctx
