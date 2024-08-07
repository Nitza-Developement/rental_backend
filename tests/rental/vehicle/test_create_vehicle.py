from django.contrib.auth import get_user_model
from django.urls import reverse

from rental.vehicle.models import Vehicle
from tests.rental.vehicle.parent_case.vehicle_api_test_case import (
    VehicleApiTestCase,
)

User = get_user_model()


class TestCreateVehicle(VehicleApiTestCase):
    def call_create_vehicle(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("vehicle")
        payload = {
            "type": "Car",
            "year": 2020,
            "make": "make",
            "model": "model",
            "trim": "trim",
            "plate": "plate",
            "vin": "vin",
            "odometer": 1,
            "nickname": "nickname",
            "spare_tires": 20,
            "extra_fields": "{}",
            "status": "Available",
        }

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
        )

    def test_create_vehicle(self):
        initial_amount = Vehicle.objects.count()

        # case not authenticated, response 401
        self.call_create_vehicle(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Vehicle.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_create_vehicle(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Vehicle.objects.count())

        # case correct, response 201
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        response_dict = self.call_create_vehicle(
            print_json_response=False,
        )
        self.assertEqual(initial_amount + 1, Vehicle.objects.count())
        self.assertEqual(True, "id" in response_dict)
        vehicle_id = response_dict["id"]

        self.assertEqual(True, "plate" in response_dict)
        plate_data = response_dict["plate"]
        self.assertEqual(True, "id" in plate_data)
        plate_id = plate_data["id"]
        self.assertEqual(True, "assign_date" in plate_data)
        assign_date = plate_data["assign_date"]

        self.assertDictEqual(
            response_dict,
            {
                "id": vehicle_id,
                "vin": "vin",
                "nickname": "nickname",
                "odometer": 1,
                "spare_tires": 20,
                "plate": {
                    "id": plate_id,
                    "plate": "plate",
                    "assign_date": assign_date,
                },
                "type": "Car",
                "year": 2020,
                "make": "make",
                "model": "model",
                "trim": "trim",
                "status": "Available",
                "tracker": None,
                "extra_fields": {},
            },
        )
