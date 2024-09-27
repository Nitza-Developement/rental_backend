import random
from typing import Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from rental.rentalPlan.models import RentalPlan
from tests.rental.rental_plan.parent_case.rental_plan_api_test_case import (
    RentalPlanApiTestCase,
)

fake = Faker()
User = get_user_model()


class TestCreateRentalPlan(RentalPlanApiTestCase):
    def call_create_rental_plan(
        self,
        name: Optional[str] = None,
        amount: Optional[int] = None,
        periodicity: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("rental-plan")
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

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
        )

    def test_create_rental_plan(self):
        initial_amount = RentalPlan.objects.count()

        # case not authenticated, response 401
        self.call_create_rental_plan(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, RentalPlan.objects.count())

        # case bad authenticated user (not admin), response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_create_rental_plan(forbidden=True)
        self.assertEqual(initial_amount, RentalPlan.objects.count())

        # case correct, response 201
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        response_dict = self.call_create_rental_plan(
            print_json_response=False,
            name="rental_plan",
            amount=123,
            periodicity=RentalPlan.WEEKLY,
        )
        self.assertEqual(initial_amount + 1, RentalPlan.objects.count())
        self.assertEqual(True, "id" in response_dict)
        rental_plan_id = response_dict["id"]
        self.assertDictEqual(
            response_dict,
            {
                "id": rental_plan_id,
                "name": "rental_plan",
                "amount": 123,
                "periodicity": RentalPlan.WEEKLY,
            },
        )

        # case bad, not unique, response 400
        self.call_create_rental_plan(
            print_json_response=False,
            name="rental_plan",
            amount=123,
            periodicity=RentalPlan.WEEKLY,
            bad_request=True,
        )
        self.assertEqual(initial_amount + 1, RentalPlan.objects.count())

        # case correct, new unique, response 201
        self.call_create_rental_plan(
            print_json_response=False,
        )
