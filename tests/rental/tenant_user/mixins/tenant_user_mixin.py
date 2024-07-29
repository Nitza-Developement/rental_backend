from typing import Optional

from django.contrib.auth import get_user_model
from faker import Faker

from rental.models import Tenant, TenantUser
from tests.rental.auth.utils.custom_test_user import CustomTestUser

faker = Faker()

User = get_user_model()


class TenantUserMixin:
    def create_tenant(self, user: User, email: Optional[str] = None) -> Tenant:
        if not email:
            email = user.email
        tenant = Tenant.objects.create(
            email=email, name=f"tenant_{email}", isAdmin=True
        )
        return tenant

    def create_tenant_user(self) -> CustomTestUser:
        password = faker.password(length=8)
        User.objects.create_user(email=faker.email(), password=password)
        tenant = Tenant.objects.create(
            email=self.admin_email, name="tenant_admin", isAdmin=True
        )
        tenant_user = TenantUser.objects.create(
            role=TenantUser.ADMIN,
            tenant=tenant,
            user=self.admin_user,
            is_default=True,
        )
        return tenant_user
