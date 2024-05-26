from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import (
    Tenant,
    Client,
    Contract,
    TollDue,
    RentalPlan,
    StageUpdate,
)
from datetime import timedelta
import random
from django.utils import timezone

from django.db import transaction

from rental.vehicle.models import VehiclePlate


def get_past_date(months=0, weeks=0, days=0):
    current_date = timezone.now()
    return (
        current_date - timedelta(weeks=weeks, days=days) - timedelta(days=30 * months)
    )


@SeederRegistry.register
class ContractSeeder(seeders.Seeder):
    id = "ContractSeeder"
    priority = 4

    @transaction.atomic
    def seed(self):
        print("Seeding contracts data...")
        tenant = 2

        clients_list = [1, 2, 3]
        rental_plan_list = [1, 2, 3]
        vehicle_list = [1, 2, 4, 6, 7, 9]

        def random_element(array):
            return random.choice(array)

        contract1 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=12),
            active_date=get_past_date(months=12, days=2),
        )
        StageUpdate.objects.create(
            contract=contract1,
            stage=StageUpdate.ACTIVE,
            date=get_past_date(months=12, days=2),
        )

        for i in range(1, 5):
            TollDue.objects.create(
                amount=100,
                plate=contract1.vehicle.plates.filter(is_active=True).first(),
                contract=contract1,
                invoiceNumber=f"M1235{i}",
                stage=TollDue.PAID,
                createDate=get_past_date(months=11, days=i * 2),
            )

        for i in range(1, 3):
            TollDue.objects.create(
                amount=500,
                plate=contract1.vehicle.plates.filter(is_active=True).first(),
                contract=contract1,
                invoiceNumber=f"X1432{i}",
                stage=TollDue.UNPAID,
                createDate=get_past_date(months=11, days=20 + i * 2),
            )

        contract2 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=7),
            active_date=get_past_date(months=6),
        )
        StageUpdate.objects.create(
            contract=contract2, stage=StageUpdate.ACTIVE, date=get_past_date(months=6)
        )

        for i in range(1, 3):
            TollDue.objects.create(
                amount=250 + i * 32,
                plate=contract2.vehicle.plates.filter(is_active=True).first(),
                contract=contract2,
                invoiceNumber=f"X1{i * 2}32{i}",
                stage=TollDue.PAID,
                createDate=get_past_date(months=4, days=15 + i * 2),
            )

        contract3 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=4),
            active_date=get_past_date(months=3),
        )
        StageUpdate.objects.create(
            contract=contract3, stage=StageUpdate.ACTIVE, date=get_past_date(months=3)
        )

        for i in range(1, 4):
            TollDue.objects.create(
                amount=250 + i * 32,
                plate=contract3.vehicle.plates.filter(is_active=True).first(),
                contract=contract3,
                invoiceNumber=f"J1{i * 2}32{i}",
                stage=TollDue.PAID,
                createDate=get_past_date(months=2, days=10 + i * 2),
            )

        TollDue.objects.create(
            amount=2400,
            plate=contract3.vehicle.plates.filter(is_active=True).first(),
            contract=contract3,
            invoiceNumber="J112321",
            stage=TollDue.UNPAID,
            createDate=get_past_date(months=1, days=29),
        )

        contract4 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=2),
            active_date=get_past_date(months=1),
        )
        StageUpdate.objects.create(
            contract=contract4, stage=StageUpdate.ACTIVE, date=get_past_date(months=1)
        )

        TollDue.objects.create(
            amount=130,
            plate=contract4.vehicle.plates.filter(is_active=True).first(),
            contract=contract4,
            invoiceNumber="Q769531",
            stage=TollDue.UNPAID,
            createDate=get_past_date(months=1, days=29),
        )

        contract5 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(weeks=3),
            active_date=get_past_date(weeks=1),
        )
        StageUpdate.objects.create(
            contract=contract5, stage=StageUpdate.ACTIVE, date=get_past_date(weeks=1)
        )

        contract6 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=12),
            active_date=get_past_date(months=12, days=2),
        )
        StageUpdate.objects.create(
            contract=contract6,
            stage=StageUpdate.ACTIVE,
            date=get_past_date(months=12, days=2),
        )
        StageUpdate.objects.create(
            contract=contract6,
            stage=StageUpdate.ENDED,
            date=get_past_date(months=6),
        )
        contract6.end_date = get_past_date(months=6)
        contract6.save()

        for i in range(1, 3):
            TollDue.objects.create(
                amount=250 + i * 32,
                plate=contract6.vehicle.plates.filter(is_active=True).first(),
                contract=contract6,
                invoiceNumber=f"N9{i * 2}47{i}",
                stage=TollDue.PAID,
                createDate=get_past_date(months=10, days=10 + i * 2),
            )

        TollDue.objects.create(
            amount=130,
            plate=contract6.vehicle.plates.filter(is_active=True).first(),
            contract=contract6,
            invoiceNumber="Z785423",
            stage=TollDue.PAID,
            createDate=get_past_date(days=25),
        )

        contract7 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=12),
            active_date=get_past_date(months=12, days=2),
        )
        StageUpdate.objects.create(
            contract=contract7,
            stage=StageUpdate.ACTIVE,
            date=get_past_date(months=12, days=2),
        )
        StageUpdate.objects.create(
            contract=contract7,
            stage=StageUpdate.ENDED,
            date=get_past_date(months=1),
        )
        contract7.end_date = get_past_date(months=1)
        contract7.save()

        for i in range(1, 4):
            TollDue.objects.create(
                amount=250 + i * 32,
                plate=contract7.vehicle.plates.filter(is_active=True).first(),
                contract=contract7,
                invoiceNumber=f"M9{i * 2}23{i}",
                stage=TollDue.PAID,
                createDate=get_past_date(months=10, days=10 + i * 2),
            )

        TollDue.objects.create(
            amount=650,
            plate=contract7.vehicle.plates.filter(is_active=True).first(),
            contract=contract7,
            invoiceNumber="H894032",
            stage=TollDue.UNPAID,
            createDate=get_past_date(weeks=1),
        )

        contract8 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=7),
            active_date=get_past_date(months=6),
        )
        StageUpdate.objects.create(
            contract=contract8, stage=StageUpdate.ACTIVE, date=get_past_date(months=6)
        )
        StageUpdate.objects.create(
            contract=contract8, stage=StageUpdate.ENDED, date=get_past_date(months=1)
        )
        contract8.end_date = get_past_date(months=1)
        contract8.save()

        TollDue.objects.create(
            amount=650,
            plate=contract8.vehicle.plates.filter(is_active=True).first(),
            contract=contract8,
            invoiceNumber="Y546782",
            stage=TollDue.UNPAID,
            createDate=get_past_date(months=3),
        )

        TollDue.objects.create(
            amount=650,
            plate=contract8.vehicle.plates.filter(is_active=True).first(),
            contract=contract8,
            invoiceNumber="Y546790",
            stage=TollDue.UNPAID,
            createDate=get_past_date(weeks=1),
        )

        contract9 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=1),
            active_date=get_past_date(months=1),
        )
        StageUpdate.objects.create(
            contract=contract9, stage=StageUpdate.ACTIVE, date=get_past_date(months=1)
        )
        StageUpdate.objects.create(
            contract=contract9, stage=StageUpdate.ENDED, date=get_past_date(days=4)
        )
        contract9.end_date = get_past_date()
        contract9.save()

        contract10 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=12),
            active_date=get_past_date(months=12),
        )
        StageUpdate.objects.create(
            contract=contract10,
            stage=StageUpdate.DISMISS,
            date=get_past_date(months=12),
        )

        contract11 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=6),
            active_date=get_past_date(months=6),
        )
        StageUpdate.objects.create(
            contract=contract11, stage=StageUpdate.DISMISS, date=get_past_date(months=6)
        )

        contract12 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=3),
            active_date=get_past_date(months=3),
        )
        StageUpdate.objects.create(
            contract=contract12, stage=StageUpdate.DISMISS, date=get_past_date(months=3)
        )

        contract13 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(months=1),
            active_date=get_past_date(months=1),
        )
        StageUpdate.objects.create(
            contract=contract13, stage=StageUpdate.DISMISS, date=get_past_date(months=1)
        )

        contract14 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(weeks=1),
            active_date=get_past_date(weeks=1),
        )
        StageUpdate.objects.create(
            contract=contract14, stage=StageUpdate.DISMISS, date=get_past_date(weeks=1)
        )

        contract15 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(weeks=1),
            active_date=get_past_date(weeks=1),
        )
        StageUpdate.objects.create(
            contract=contract15, stage=StageUpdate.PENDING, date=get_past_date(weeks=1)
        )

        contract16 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=get_past_date(days=1),
            active_date=get_past_date(days=1),
        )
        StageUpdate.objects.create(
            contract=contract16, stage=StageUpdate.PENDING, date=get_past_date(days=1)
        )

        contract17 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=timezone.now(),
            active_date=timezone.now(),
        )
        StageUpdate.objects.create(
            contract=contract17, stage=StageUpdate.PENDING, date=timezone.now()
        )

        contract18 = Contract.objects.create(
            tenant_id=tenant,
            rental_plan_id=random_element(rental_plan_list),
            client_id=random_element(clients_list),
            vehicle_id=random_element(vehicle_list),
            creation_date=timezone.now(),
            active_date=timezone.now(),
        )
        StageUpdate.objects.create(
            contract=contract18, stage=StageUpdate.PENDING, date=timezone.now()
        )
        print("Seeding complete!")
