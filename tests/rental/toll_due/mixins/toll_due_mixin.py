import random

from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from faker import Faker

from rental.contract.models import Contract
from rental.toll.models import TollDue
from rental.vehicle.models import VehiclePlate

fake = Faker()

User = get_user_model()


class TollDueMixin:
    def create_toll_due(
        self,
        user: User,
        plate: VehiclePlate,
        contract: Contract,
    ) -> TollDue:
        with set_actor(user):
            return TollDue.objects.create(
                plate=plate,
                contract=contract,
                invoice=fake.uuid4(),
                invoiceNumber=fake.random_int(min=1000, max=9999),
                note=fake.text(max_nb_chars=200),
                stage=random.choice([TollDue.PAID, TollDue.UNPAID]),
                amount=random.randint(1, 1000),
            )
