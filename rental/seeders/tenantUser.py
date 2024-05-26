from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import TenantUser, Tenant, User


@SeederRegistry.register
class TenantUserSeeder(seeders.ModelSeeder):
    id = "TenantUserSeeder"
    priopity = 2
    model = TenantUser
    data = [
        {
            "role": "Admin",
            "tenant": 1,
            "user": {
                "email": "admin@admin.com",
                "name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
            "is_default": True,
        },
        {
            "role": "Admin",
            "tenant": 2,
            "user": {
                "email": "test-admin@admin.com",
                "name": "Admin-Test",
                "is_staff": True,
                "is_superuser": True,
            },
            "is_default": True,
        },
    ]

    def seed(self):
        for item in self.data:
            tenant_id = item["tenant"]
            tenant_instance = Tenant.objects.get(id=tenant_id)
            item["tenant"] = tenant_instance

            user_instance = User.objects.get_or_create(
                email=item["user"]["email"],
                defaults={
                    "name": item["user"]["name"],
                    "is_staff": item["user"]["is_staff"],
                    "is_superuser": item["user"]["is_superuser"],
                },
            )[0]
            user_instance.set_password("12345678")
            user_instance.save()

            item["user"] = user_instance
            TenantUser.objects.create(**item)
