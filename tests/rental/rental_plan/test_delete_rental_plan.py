from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.rentalPlan.models import RentalPlan
from tests.rental.rental_plan.parent_case.rental_plan_api_test_case import (
    RentalPlanApiTestCase,
)

User = get_user_model()


class TestDeleteRentalPlan(RentalPlanApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.custom_tenant_user_staff.default_tenant_user.user
        self.list_rental_plan = [
            self.create_rental_plan(user=user) for _ in range(2)
        ]

    def call_delete_rental_plan(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("rental-plan-actions", args=[entity_id])
        self.call_delete(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

    def test_delete_rental_plan(self):
        initial_amount = RentalPlan.objects.filter().count()

        # case not loguin, response 401
        self.call_delete_rental_plan(
            entity_id=self.list_rental_plan[0].id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount, RentalPlan.objects.filter().count())

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_delete_rental_plan(
            entity_id=self.list_rental_plan[0].id, forbidden=True
        )
        self.assertEqual(initial_amount, RentalPlan.objects.filter().count())

        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_delete_rental_plan(
            entity_id=99999,
            not_found=True,
        )
        self.assertEqual(initial_amount, RentalPlan.objects.filter().count())

        # case correct, response 200
        id_to_delete = self.list_rental_plan[1].id
        self.assertEqual(
            True,
            RentalPlan.objects.filter(id=id_to_delete).exists(),
        )
        self.call_delete_rental_plan(
            entity_id=id_to_delete,
        )
        self.assertEqual(
            initial_amount - 1, RentalPlan.objects.filter().count()
        )
        self.assertEqual(
            False,
            RentalPlan.objects.filter(id=id_to_delete).exists(),
        )
