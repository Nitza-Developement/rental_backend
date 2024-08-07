import random
from typing import Optional

from django.urls import reverse
from faker import Faker

from rental.vehicle.models import Vehicle, VehiclePlate
from tests.rental.vehicle.parent_case.vehicle_api_test_case import (
    VehicleApiTestCase,
)

fake = Faker()


class TestUpdateVehicle(VehicleApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.list_vehicle = [
            self.create_vehicle(user=user),
            self.create_vehicle(user=user),
        ]

    def call_update_vehicle(
        self,
        entity_id: int,
        vin: Optional[str] = None,
        plate: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("vehicle-actions", args=[entity_id])
        # print(URL)
        if not vin:
            vin = (fake.vin(),)  # Vehicle identification number
        if not plate:
            plate = (
                fake.license_plate(),
            )  # License plate (random license plate)
        payload = {
            "type": random.choice(
                [
                    Vehicle.CAR,
                    Vehicle.SUV,
                    Vehicle.FREIGHTLINER,
                    Vehicle.TRAILER,
                    Vehicle.TRUCK,
                    Vehicle.VAN,
                    Vehicle.CUSTOM,
                ]
            ),
            "year": random.randint(1990, 2023),  # Year between 1990 and 2023
            "make": fake.company(),  # Manufacturer
            "model": fake.word().capitalize(),  # Model (a random word)
            "trim": fake.word().capitalize(),  # Trim (another random word)
            "plate": plate,
            "vin": vin,
            "odometer": random.randint(
                0, 200000
            ),  # Odometer (value between 0 and 200,000 miles)
            "nickname": fake.first_name(),  # Nickname (random name)
            "spare_tires": random.randint(0, 5),  # Spare wheels between 0 and 5
            "extra_fields": "",  # ,"{}",
            "status": random.choice(
                [
                    Vehicle.AVAILABLE,
                    Vehicle.UNAVAILABLE,
                    Vehicle.RENTED,
                    Vehicle.IN_MAINTENANCE,
                ]
            ),  # Random state
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
            self.validate_vehicle_in_list(
                data=response_dict,
                vehicle_id=entity_id,
            )
        return response_dict

    def test_update_vehicle(self):
        initial_amount_vehicle = Vehicle.objects.count()
        initial_amount_plate = VehiclePlate.objects.count()
        vehicle = self.list_vehicle[0]

        # case not authenticated, response 401
        self.call_update_vehicle(
            entity_id=vehicle.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(initial_amount_plate, VehiclePlate.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_update_vehicle(
            entity_id=vehicle.id,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(initial_amount_plate, VehiclePlate.objects.count())

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_vehicle(
            entity_id=999999,
            not_found=True,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(initial_amount_plate, VehiclePlate.objects.count())

        # case correct, same plate, response 200
        old_plate: VehiclePlate = VehiclePlate.objects.filter(
            vehicle=vehicle
        ).first()
        self.assertIsNotNone(old_plate)
        self.call_update_vehicle(
            entity_id=vehicle.id,
            plate=old_plate.plate,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(initial_amount_plate, VehiclePlate.objects.count())

        # case correct,new plate, response 200
        create_plate = 1
        self.assertEqual(
            1, VehiclePlate.objects.filter(vehicle=vehicle).count()
        )
        self.assertTrue(old_plate.is_active)
        self.call_update_vehicle(
            entity_id=vehicle.id,
            plate="newplate",
            print_json_response=False,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(
            initial_amount_plate + create_plate, VehiclePlate.objects.count()
        )
        self.assertEqual(
            2, VehiclePlate.objects.filter(vehicle=vehicle).count()
        )
        self.assertEqual(
            1,
            VehiclePlate.objects.filter(
                vehicle=vehicle, is_active=True
            ).count(),
        )
        new_plate: VehiclePlate = VehiclePlate.objects.filter(
            vehicle=vehicle, is_active=True
        ).first()
        self.assertIsNotNone(new_plate)
        self.assertTrue("newplate", new_plate.plate)

        # case bad, not unique vin, response 400
        other_vehicle = self.list_vehicle[1]
        self.call_update_vehicle(
            entity_id=vehicle.id,
            vin=other_vehicle.vin,
            bad_request=True,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(
            initial_amount_plate + create_plate, VehiclePlate.objects.count()
        )

        # case bad, not unique plate, response 400
        other_vehicle = self.list_vehicle[1]
        self.call_update_vehicle(
            entity_id=vehicle.id,
            plate=VehiclePlate.objects.filter(vehicle=other_vehicle)
            .first()
            .plate,
            bad_request=True,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_vehicle, Vehicle.objects.count())
        self.assertEqual(
            initial_amount_plate + create_plate, VehiclePlate.objects.count()
        )
