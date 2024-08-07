import random
from typing import Dict, Optional

from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from faker import Faker

from rental.vehicle.models import Vehicle, VehiclePlate
from tests.util.date_treatment import get_datetime_str_form_in_proper_area

fake = Faker()

User = get_user_model()


class VehicleMixin:
    def create_vehicle(self, user: Optional[User] = None) -> Vehicle:
        if not user:
            user = self.custom_user.user
        with set_actor(user):
            new_vehicle = Vehicle.objects.create(
                type=random.choice(
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
                year=random.randint(1990, 2023),  # Year between 1990 and 2023
                make=fake.company(),  # Manufacturer
                model=fake.word().capitalize(),  # Model (a random word)
                trim=fake.word().capitalize(),  # Trim (another random word)
                vin=fake.vin(),  # Vehicle identification number
                odometer=random.randint(
                    0, 200000
                ),  # Odometer (value between 0 and 200,000 miles)
                nickname=fake.word().capitalize(),  # Nickname (random name)
                spare_tires=random.randint(
                    0, 5
                ),  # Spare wheels between 0 and 5
                extra_fields={},
                status=random.choice(
                    [
                        Vehicle.AVAILABLE,
                        Vehicle.UNAVAILABLE,
                        Vehicle.RENTED,
                        Vehicle.IN_MAINTENANCE,
                    ]
                ),  # Estado aleatorio
                tenant=user.defaultTenantUser().tenant,
            )

            VehiclePlate.objects.create(
                vehicle=new_vehicle,
                plate=fake.license_plate(),  # License plate (random license plate)
            )
            return new_vehicle

    def validate_vehicle_in_list(
        self,
        data: Dict,
        vehicle_id: Optional[int] = None,
        plate: Optional[VehiclePlate] = None,
    ):
        if not vehicle_id:
            self.assertEqual(True, "id" in data)
            vehicle_id = data["id"]
        if not plate:
            self.assertEqual(True, "plate" in data)
            plate_data = data["plate"]
            self.assertEqual(True, "id" in plate_data)
            plate_id = plate_data["id"]
            plate: VehiclePlate = VehiclePlate.objects.filter(
                id=plate_id
            ).first()
            self.assertIsNotNone(plate)

        vehicle: Vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        self.assertIsNotNone(vehicle)

        self.assertDictEqual(
            data,
            {
                "id": vehicle.id,
                "vin": vehicle.vin,
                "nickname": vehicle.nickname,
                "odometer": vehicle.odometer,
                "spare_tires": vehicle.spare_tires,
                "plate": {
                    "id": plate.id,
                    "plate": plate.plate,
                    "assign_date": get_datetime_str_form_in_proper_area(
                        plate.assign_date
                    ),  # .strftime('%d-%m-%Y - %H:%M:%S'),
                },
                "type": vehicle.type,
                "year": vehicle.year,
                "make": vehicle.make,
                "model": vehicle.model,
                "trim": vehicle.trim,
                "status": vehicle.status,
                "tracker": None,
                "extra_fields": {},
            },
        )
