from django_seeding import seeders
from rental.models import RentalPlan
from django_seeding.seeder_registry import SeederRegistry


@SeederRegistry.register
class RentalPlanSeeder(seeders.ModelSeeder):
    id = "RentalPlanSeeder"
    priority = 3
    model = RentalPlan
    tenant = 2
    data = [
        {
            "id": 1,
            "name": "Monthly trailer rental",
            "periodicity": RentalPlan.MONTHLY,
            "amount": 1000,
            "tenant_id": tenant,
        },
        {
            "id": 2,
            "name": "Biweekly trailer rental",
            "periodicity": RentalPlan.BIWEEKLY,
            "amount": 500,
            "tenant_id": tenant,
        },
        {
            "id": 3,
            "name": "Weekly trailer rental",
            "periodicity": RentalPlan.WEEKLY,
            "amount": 250,
            "tenant_id": tenant,
        },
    ]
