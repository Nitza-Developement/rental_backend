from typing import Dict, Optional

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

    def validate_tenant_user_in_list(
        self, data: Dict, tenant_user_id: Optional[int] = None
    ):
        if not tenant_user_id:
            self.assertEqual(True, "id" in data)
            tenant_user_id = data["id"]
        tenant_user: TenantUser = TenantUser.objects.filter(
            id=tenant_user_id
        ).first()
        self.assertIsNotNone(tenant_user)
        user: User = tenant_user.user
        self.assertIsNotNone(user)
        tenant: Tenant = tenant_user.tenant
        self.assertIsNotNone(tenant)
        tenant_user_owner: TenantUser = tenant.owner()
        if tenant_user_owner:
            user_in_tenant_user_owner: User = tenant_user_owner.user
            self.assertIsNotNone(user_in_tenant_user_owner)
            owner = {
                "id": tenant_user_owner.id,
                "role": tenant_user_owner.role,
                "user": {
                    "id": user_in_tenant_user_owner.id,
                    "name": user_in_tenant_user_owner.name,
                    "email": user_in_tenant_user_owner.email,
                    "image": None,  # user_in_tenant_user_owner.image,
                },
            }
        else:
            owner = {
                "role": None,
                "user": {"name": "", "email": "", "image": None},
            }

        self.assertDictEqual(
            data,
            {
                "id": tenant_user_id,
                "role": tenant_user.role,
                "tenant": {
                    "id": tenant.id,
                    "email": tenant.email,
                    "name": tenant.name,
                    "isAdmin": tenant.isAdmin,
                    "owner": owner,
                    "tenantUsers": [
                        {
                            "id": tenant_user_id,
                            "role": tenant_user.role,
                            "user": {
                                "id": user.id,
                                "name": user.name,
                                "email": user.email,
                                "image": None,
                            },
                        }
                    ],
                },
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "image": None,
                },
                "is_default": tenant_user.is_default,
            },
        )
