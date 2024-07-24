from datetime import timedelta
import random
from django.utils import timezone
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import (
    Tenant,
    Client,
    Contract,
    TollDue,
    RentalPlan,
    StageUpdate,
    Vehicle,
)

from rental.vehicle.models import VehiclePlate


def get_past_date(months=0, weeks=0, days=0):
    current_date = timezone.now()
    return (
        current_date - timedelta(weeks=weeks, days=days) - timedelta(days=30 * months)
    )


@SeederRegistry.register
class ContractSeeder(seeders.Seeder):
    id = "ContractSeeder"
    priority = 8

    def seed(self):
        tenant = Tenant.objects.first()

        clients = Client.objects.all()
        rental_plans = RentalPlan.objects.all()
        vehicles = Vehicle.objects.all()

        def random_element(array):
            return random.choice(array)

        for i in range(1, 20):

            contract = Contract.objects.create(
                tenant=tenant,
                rental_plan=random_element(rental_plans),
                client=random_element(clients),
                vehicle=random_element(vehicles),
                creation_date=get_past_date(months=12),
                active_date=get_past_date(months=12, days=2),
            )

            StageUpdate.objects.create(
                contract=contract,
                stage=StageUpdate.ACTIVE,
                date=get_past_date(months=12, days=2),
            )

            plate = VehiclePlate.objects.filter(vehicle=contract.vehicle).first()

            for i in range(1, 5):
                TollDue.objects.create(
                    amount=100,
                    plate=plate,
                    contract=contract,
                    invoiceNumber=f"M1235{i}",
                    stage=TollDue.PAID,
                    createDate=get_past_date(months=11, days=i * 2),
                )

            for i in range(1, 3):
                TollDue.objects.create(
                    amount=500,
                    plate=plate,
                    contract=contract,
                    invoiceNumber=f"X1432{i}",
                    stage=TollDue.UNPAID,
                    createDate=get_past_date(months=11, days=20 + i * 2),
                )
