from django_seeding.seeder_registry import SeederRegistry
from django_seeding import seeders
from rental.models import Tenant


@SeederRegistry.register
class TenantSeeder(seeders.ModelSeeder):
    id = "TenantSeeder"
    priority = 1
    model = Tenant
    data = [
        {"email": "admin@tenant.com", "name": "Admin-Tenant", "isAdmin": True},
        {"email": "test@tenant.com", "name": "Test-Tenant"},
    ]
