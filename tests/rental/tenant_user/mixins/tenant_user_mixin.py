from typing import Optional

from django.contrib.auth import get_user_model
from faker import Faker

from rental.models import Tenant, TenantUser
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)

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

    def create_tenant_user(self) -> CustomTenantTestUser:
        email = faker.email()
        password = faker.password(length=8)
        user = User.objects.create_user(email=email, password=password)
        tenant = Tenant.objects.create(email=email, name=email, isAdmin=True)
        tenant_user = TenantUser.objects.create(
            role=TenantUser.OWNER,
            tenant=tenant,
            user=user,
            is_default=True,
        )
        return CustomTenantTestUser(tenant_user=tenant_user, password=password)
