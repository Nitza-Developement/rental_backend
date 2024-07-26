from django_seeding.seeder_registry import SeederRegistry
from django_seeding import seeders
from rental.models import RentalPlan, Tenant

tenant = Tenant.objects.first()


@SeederRegistry.register
class RentalPlanSeeder(seeders.ModelSeeder):
    id = "RentalPlanSeeder"
    priority = 3
    model = RentalPlan
    data = [
        {
            "name": "Monthly trailer rental",
            "periodicity": RentalPlan.MONTHLY,
            "amount": 1000,
            "tenant": tenant,
        },
        {
            "name": "Biweekly trailer rental",
            "periodicity": RentalPlan.BIWEEKLY,
            "amount": 500,
            "tenant": tenant,
        },
        {
            "name": "Weekly trailer rental",
            "periodicity": RentalPlan.WEEKLY,
            "amount": 250,
            "tenant": tenant,
        },
    ]
