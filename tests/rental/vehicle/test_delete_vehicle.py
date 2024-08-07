from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.vehicle.models import Vehicle
from tests.rental.vehicle.parent_case.vehicle_api_test_case import (
    VehicleApiTestCase,
)

User = get_user_model()


class TestDeleteVehicle(VehicleApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.custom_tenant_user_staff.default_tenant_user.user
        self.list_vehicle = [self.create_vehicle(user=user) for _ in range(2)]

    def call_delete_vehicle(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("vehicle-actions", args=[entity_id])
        self.call_delete(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )

    def test_delete_tenant(self):
        initial_amount = Vehicle.objects.filter(is_deleted=False).count()

        # case not loguin, response 401
        self.call_delete_vehicle(
            entity_id=self.list_vehicle[0].id,
            unauthorized=True,
        )
        self.assertEqual(
            initial_amount, Vehicle.objects.filter(is_deleted=False).count()
        )

        # case not admin, response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_delete_vehicle(
            entity_id=self.list_vehicle[0].id, forbidden=True
        )
        self.assertEqual(
            initial_amount, Vehicle.objects.filter(is_deleted=False).count()
        )

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_delete_vehicle(
            entity_id=99999,
            not_found=True,
        )
        self.assertEqual(
            initial_amount, Vehicle.objects.filter(is_deleted=False).count()
        )

        # case correct, response 200
        id_to_delete = self.list_vehicle[1].id
        self.assertEqual(
            True,
            Vehicle.objects.filter(id=id_to_delete, is_deleted=False).exists(),
        )
        self.call_delete_vehicle(
            entity_id=id_to_delete,
        )
        self.assertEqual(
            initial_amount - 1, Vehicle.objects.filter(is_deleted=False).count()
        )
        self.assertEqual(
            False,
            Vehicle.objects.filter(id=id_to_delete, is_deleted=False).exists(),
        )
