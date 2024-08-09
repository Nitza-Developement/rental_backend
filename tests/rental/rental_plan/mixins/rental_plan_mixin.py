import random
from typing import Dict, Optional

from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from faker import Faker

from rental.rentalPlan.models import RentalPlan

fake = Faker()

User = get_user_model()


class RentalPlanMixin:
    def create_rental_plan(
        self,
        name: Optional[str] = None,
        amount: Optional[int] = None,
        periodicity: Optional[str] = None,
        user: Optional[User] = None,
    ) -> RentalPlan:
        if not user:
            user = self.custom_staff.user
        if not name:
            name = fake.text(max_nb_chars=30)
        if not amount:
            amount = random.randint(1, 1000)
        if not periodicity:
            periodicity = random.choice(
                [RentalPlan.WEEKLY, RentalPlan.BIWEEKLY, RentalPlan.MONTHLY]
            )
        with set_actor(user):
            return RentalPlan.objects.create(
                name=name,
                amount=amount,
                periodicity=periodicity,
                tenant=user.defaultTenantUser().tenant,
            )

    def validate_rental_plan_in_list(
        self,
        data: Dict,
        rental_plan_id: Optional[int] = None,
    ):
        if not rental_plan_id:
            self.assertEqual(True, "id" in data)
            rental_plan_id = data["id"]

        rental_plan: RentalPlan = RentalPlan.objects.filter(
            id=rental_plan_id
        ).first()
        self.assertIsNotNone(rental_plan)

        self.assertDictEqual(
            data,
            {
                "id": rental_plan_id,
                "name": rental_plan.name,
                "amount": rental_plan.amount,
                "periodicity": rental_plan.periodicity,
            },
        )
