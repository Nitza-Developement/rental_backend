import random
from typing import Any, Dict, Optional

from auditlog.models import LogEntry
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from rental.vehicle.features import update_vehicle
from rental.vehicle.models import Vehicle, VehiclePlate
from tests.rental.vehicle.parent_case.vehicle_api_test_case import (
    VehicleApiTestCase,
)
from tests.util.faker_values import get_different_from

fake = Faker()
User = get_user_model()


class TestHistoryVehicle(VehicleApiTestCase):
    def setUp(self):
        super().setUp()
        self.user_vehicle = self.create_tenant_user().default_tenant_user.user
        self.list_vehicle = [
            self.create_vehicle(user=self.user_vehicle),
            self.create_vehicle(user=self.user_vehicle),
        ]
        for _ in range(3):
            for i in range(len(self.list_vehicle)):
                self.list_vehicle[i] = self.custom_update_vehicle(
                    vehicle=self.list_vehicle[i], user=self.user_vehicle
                )

    def custom_update_vehicle(self, vehicle: Vehicle, user: User) -> Vehicle:
        return update_vehicle(
            vehicle=vehicle,
            user=user,
            type=get_different_from(
                vehicle.type,
                lambda: random.choice(
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
            ),
            year=get_different_from(
                vehicle.year, lambda: random.randint(1990, 2023)
            ),  # Year between 1990 and 2023
            make=get_different_from(
                vehicle.make, lambda: fake.company()
            ),  # Manufacturer
            model=get_different_from(
                vehicle.model, lambda: fake.word().capitalize()
            ),  # Model (a random word)
            trim=get_different_from(
                vehicle.trim, lambda: fake.word().capitalize()
            ),  # Trim (another random word)
            vin=get_different_from(
                vehicle.vin, lambda: fake.vin()
            ),  # Vehicle identification number
            odometer=get_different_from(
                vehicle.odometer, lambda: random.randint(0, 200000)
            ),  # Odometer (value between 0 and 200,000 miles)
            nickname=get_different_from(
                vehicle.nickname, lambda: fake.word().capitalize()
            ),  # Nickname (random name)
            spare_tires=get_different_from(
                vehicle.spare_tires, lambda: random.randint(0, 5)
            ),  # Spare wheels between 0 and 5
            extra_fields={},
            status=get_different_from(
                vehicle.status,
                lambda: random.choice(
                    [
                        Vehicle.AVAILABLE,
                        Vehicle.UNAVAILABLE,
                        Vehicle.RENTED,
                        Vehicle.IN_MAINTENANCE,
                    ]
                ),
            ),  # Estado aleatorio
            plate=get_different_from(
                VehiclePlate.objects.filter(is_active=True, vehicle=vehicle)
                .first()
                .plate,
                lambda: fake.license_plate(),
            ),
        )

    def call_history_vehicle(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        URL = reverse("vehicle-actions-history", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        self.assertTrue(True, isinstance(response_dict, list))
        for history in response_dict:
            self.validate_history_vehicle(data=history)

        return response_dict

    def validate_history_vehicle(self, data: Dict[str, Any]):
        action = self.assertKey(
            data,
            "action",
            expected_any=[
                LogEntry.Action.CREATE,
                LogEntry.Action.UPDATE,
                LogEntry.Action.DELETE,
                LogEntry.Action.ACCESS,
            ],
        )
        model = self.assertKey(
            data, "model", expected_any=["vehicle", "plate", "picture"]
        )
        changes = self.assertKey(data, "changes", expected_type=dict)

        if model == "vehicle":
            list_keys_changes = [
                "year",
                "make",
                "model",
                "trim",
                "vin",
                "odometer",
                "nickname",
                "status",
                "type",
            ]
        elif model == "plate":
            if action == LogEntry.Action.CREATE:
                list_keys_changes = [
                    "plate",
                    "vehicle",
                    "is active",
                    "toll_dues",
                    "assign date",
                ]
            else:
                list_keys_changes = [
                    "is active",
                    "dismiss date",
                ]
        else:
            list_keys_changes = [
                "image",
                "vehicle",
                "pinned",
            ]
        if action == LogEntry.Action.CREATE:
            list_keys_changes += ["ID"]
        for key in list_keys_changes:
            self.assertKey(changes, key, expected_in_list_of_type=[str, str])
        self.assertKey(data, "timestamp", expected_none=False)
        user = self.user_vehicle
        self.assertKey(
            data,
            "actor",
            expected_dict={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": None,
            },
        )

    def test_history_vehicle(self):
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        for entity in self.list_vehicle:
            # case correct, response 200
            self.call_history_vehicle(
                entity_id=entity.id, print_json_response=False
            )
