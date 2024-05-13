from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import Tenant


@SeederRegistry.register
class TenantSeeder(seeders.ModelSeeder):
    id = 'TenantSeeder'
    priopity = 1
    model = Tenant
    data = [
        {
            "id": 1,
            "email": "admin@tenant.com",
            "name": "Admin-Tenant",
            "isAdmin": True
        },
        {
            "id": 2,
            "email": "test@tenant.com",
            "name": "Test-Tenant"
        },
    ]


