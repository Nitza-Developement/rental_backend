import random
from typing import Optional

from django.urls import reverse
from faker import Faker

from rental.rentalPlan.models import RentalPlan
from tests.rental.rental_plan.parent_case.rental_plan_api_test_case import (
    RentalPlanApiTestCase,
)

fake = Faker()


class TestUpdateRentalPlan(RentalPlanApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.list_rental_plan = [
            self.create_rental_plan(user=user),
            self.create_rental_plan(user=user),
        ]

    def call_update_rental_plan(
        self,
        entity_id: int,
        name: Optional[str] = None,
        amount: Optional[int] = None,
        periodicity: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("rental-plan-actions", args=[entity_id])
        # print(URL)
        if not name:
            name = fake.text(max_nb_chars=30)
        if not amount:
            amount = random.randint(1, 1000)
        if not periodicity:
            periodicity = random.choice(
                [RentalPlan.WEEKLY, RentalPlan.BIWEEKLY, RentalPlan.MONTHLY]
            )
        payload = {
            "name": name,
            "amount": amount,
            "periodicity": periodicity,
        }
        response_dict = self.call_update(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_rental_plan_in_list(
                data=response_dict,
                rental_plan_id=entity_id,
            )
        return response_dict

    def test_update_rental_plan(self):
        initial_amount_rental_plan = RentalPlan.objects.count()
        rental_plan = self.list_rental_plan[0]

        # case not authenticated, response 401
        self.call_update_rental_plan(
            entity_id=rental_plan.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_rental_plan, RentalPlan.objects.count())

        # case bad authenticated user (not admin), response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_update_rental_plan(entity_id=rental_plan.id, forbidden=True)
        self.assertEqual(initial_amount_rental_plan, RentalPlan.objects.count())

        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_rental_plan(
            entity_id=999999, not_found=True, print_json_response=False
        )
        self.assertEqual(initial_amount_rental_plan, RentalPlan.objects.count())

        # case correct, response 200
        self.call_update_rental_plan(
            entity_id=rental_plan.id,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_rental_plan, RentalPlan.objects.count())

        # case bad, not unique, response 400
        other_rental_plan = self.list_rental_plan[1]
        self.call_update_rental_plan(
            entity_id=rental_plan.id,
            name=other_rental_plan.name,
            amount=other_rental_plan.amount,
            periodicity=other_rental_plan.periodicity,
            bad_request=True,
        )
        self.assertEqual(initial_amount_rental_plan, RentalPlan.objects.count())
