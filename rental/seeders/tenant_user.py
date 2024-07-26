import random
from django_seeding.seeder_registry import SeederRegistry
from django_seeding import seeders
from rental.models import TenantUser, Tenant, User


@SeederRegistry.register
class TenantUserSeeder(seeders.Seeder):
    id = "TenantUserSeeder"
    priority = 2

    def seed(self):
        data = [
            {
                "role": "Admin",
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
                "user": {
                    "email": "test-admin@admin.com",
                    "name": "Admin-Test",
                    "is_staff": True,
                    "is_superuser": True,
                },
                "is_default": True,
            },
        ]

        tenants = list(Tenant.objects.all())

        for item in data:

            tenant = random.choice(tenants)
            tenants.remove(tenant)

            item["tenant"] = tenant

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
