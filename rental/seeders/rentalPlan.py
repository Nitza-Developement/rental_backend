from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import Tenant
from rental.models import RentalPlan


@SeederRegistry.register
class RentalPlanSeeder(seeders.ModelSeeder):
    id = "RentalPlanSeeder"
    priority = 1
    model = RentalPlan
    tenant = Tenant.objects.get(id=2)
    data = [
        {
            "id": 1,
            "name": "Monthly trailer rental",
            "periodicity": RentalPlan.MONTHLY,
            "amount": 1000,
            "tenant": tenant,
        },
        {
            "id": 2,
            "name": "Biweekly trailer rental",
            "periodicity": RentalPlan.BIWEEKLY,
            "amount": 500,
            "tenant": tenant,
        },
        {
            "id": 3,
            "name": "Weekly trailer rental",
            "periodicity": RentalPlan.WEEKLY,
            "amount": 250,
            "tenant": tenant,
        },
    ]
