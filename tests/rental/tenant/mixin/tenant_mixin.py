from typing import Dict, List, Optional

from django.contrib.auth import get_user_model
from faker import Faker

from rental.models import Tenant, TenantUser

faker = Faker()

User = get_user_model()


class TenantMixin:
    def create_tenant(self, user: User, email: Optional[str] = None) -> Tenant:
        if not email:
            email = user.email
        tenant = Tenant.objects.create(
            email=email, name=f"tenant_{email}", isAdmin=True
        )
        return tenant

    def validate_tenant_in_list(
        self,
        data: Dict,
        tenant_id: int,
        tenant_user_owner: Optional[TenantUser] = None,
        tenant_users: Optional[List] = None,
    ):
        if not tenant_id:
            self.assertEqual(True, "id" in data)
            tenant_id = data["id"]
        tenant: Tenant = Tenant.objects.filter(id=tenant_id).first()
        self.assertIsNotNone(tenant)
        if tenant_users is None:
            tenant_users = TenantUser.objects.filter(tenant=tenant)
        if not tenant_user_owner:
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
                "id": tenant.id,
                "email": tenant.email,
                "name": tenant.name,
                "isAdmin": tenant.isAdmin,
                "owner": owner,
                "tenantUsers": [
                    {
                        "id": tenant_user.id,
                        "role": tenant_user.role,
                        "user": {
                            "id": tenant_user.user.id,
                            "name": tenant_user.user.name,
                            "email": tenant_user.user.email,
                            "image": None,
                        },
                    }
                    for tenant_user in tenant_users
                ],
            },
        )
