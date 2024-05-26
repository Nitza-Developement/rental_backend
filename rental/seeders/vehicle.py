from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import Tenant
from rental.vehicle.models import Vehicle, VehiclePlate, VehiclePicture


@SeederRegistry.register
class VehicleSeeder(seeders.ModelSeeder):
    id = "VehicleSeeder"
    priority = 4
    tenant = 2
    model = Vehicle
    data = [
        {
            "id": 1,
            "type": "Car",
            "year": 2024,
            "make": "Hyundai",
            "model": "Elantra",
            "trim": "SE",
            "vin": "98765432109876543",
            "odometer": 5000,
            "nickname": "El Ahorrador",
            "status": "AVAILABLE",
            "spare_tires": 1,
            "tenant_id": tenant,
        },
        {
            "id": 2,
            "type": "SUV",
            "year": 2023,
            "make": "Toyota",
            "model": "RAV4",
            "trim": "XLE",
            "vin": "12345678901234567",
            "odometer": 15000,
            "nickname": "The Adventurer",
            "status": "RENTED",
            "spare_tires": 1,
            "tenant_id": tenant,
        },
        {
            "id": 3,
            "type": "Truck",
            "year": 2022,
            "make": "Ford",
            "model": "F-150",
            "trim": "Lariat",
            "vin": "23456789012345678",
            "odometer": 25000,
            "nickname": "Big Blue",
            "status": "IN MAINTENANCE",
            "spare_tires": 2,
            "tenant_id": tenant,
        },
        {
            "id": 4,
            "type": "Car",
            "year": 2021,
            "make": "Honda",
            "model": "Civic",
            "trim": "EX",
            "vin": "34567890123456789",
            "odometer": 30000,
            "nickname": "Civvy",
            "status": "AVAILABLE",
            "spare_tires": 1,
            "tenant_id": tenant,
        },
        {
            "id": 5,
            "type": "Van",
            "year": 2020,
            "make": "Dodge",
            "model": "Grand Caravan",
            "trim": "SXT",
            "vin": "45678901234567890",
            "odometer": 45000,
            "nickname": "Family Mover",
            "status": "RENTED",
            "spare_tires": 1,
            "tenant_id": tenant,
        },
        {
            "id": 6,
            "type": "Car",
            "year": 2023,
            "make": "Chevrolet",
            "model": "Malibu",
            "trim": "LT",
            "vin": "56789012345678901",
            "odometer": 20000,
            "nickname": "Mali",
            "status": "AVAILABLE",
            "spare_tires": 1,
            "tenant_id": tenant,
        },
        {
            "id": 7,
            "type": "SUV",
            "year": 2019,
            "make": "Nissan",
            "model": "Rogue",
            "trim": "SL",
            "vin": "67890123456789012",
            "odometer": 50000,
            "nickname": "Rogue One",
            "status": "IN MAINTENANCE",
            "spare_tires": 2,
            "tenant_id": tenant,
        },
    ]


@SeederRegistry.register
class VehiclePictureSeeder(seeders.ModelSeeder):
    id = "VehiclePictureSeeder"
    priority = 6
    model = VehiclePicture
    data = [
        {
            "id": 1,
            "vehicle_id": 1,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 2,
            "vehicle_id": 2,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 3,
            "vehicle_id": 3,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 4,
            "vehicle_id": 4,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 5,
            "vehicle_id": 5,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 6,
            "vehicle_id": 6,
            "image": "sample1",
            "pinned": True,
        },
        {
            "id": 7,
            "vehicle_id": 7,
            "image": "sample1",
            "pinned": True,
        },
    ]


@SeederRegistry.register
class VehiclePlateSeeder(seeders.ModelSeeder):
    id = "VehiclePlateSeeder"
    priority = 5
    model = VehiclePlate
    data = [
        {
            "id": 1,
            "vehicle_id": 1,
            "is_active": True,
            "plate": "ABC1234",
            "assign_date": "2023-06-01T08:30:00Z",
            "dismiss_date": None,
        },
        {
            "id": 2,
            "vehicle_id": 2,
            "is_active": True,
            "plate": "XYZ5678",
            "assign_date": "2022-08-15T09:45:00Z",
            "dismiss_date": None,
        },
        {
            "id": 3,
            "vehicle_id": 3,
            "is_active": True,
            "plate": "LMN4321",
            "assign_date": "2021-12-05T07:20:00Z",
            "dismiss_date": None,
        },
        {
            "id": 4,
            "vehicle_id": 4,
            "is_active": True,
            "plate": "QWE9876",
            "assign_date": "2020-10-11T11:10:00Z",
            "dismiss_date": None,
        },
        {
            "id": 5,
            "vehicle_id": 5,
            "is_active": False,
            "plate": "ASD5432",
            "assign_date": "2019-07-23T13:30:00Z",
            "dismiss_date": "2022-09-01T14:00:00Z",
        },
        {
            "id": 6,
            "vehicle_id": 6,
            "is_active": True,
            "plate": "ASD5439",
            "assign_date": "2022-09-01T20:00:00Z",
            "dismiss_date": None,
        },
        {
            "id": 7,
            "vehicle_id": 7,
            "is_active": True,
            "plate": "JKL3210",
            "assign_date": "2023-02-27T16:15:00Z",
            "dismiss_date": None,
        },
        {
            "id": 8,
            "vehicle_id": 3,
            "is_active": False,
            "plate": "MNB0987",
            "assign_date": "2018-04-14T10:05:00Z",
            "dismiss_date": "2021-11-30T09:50:00Z",
        },
        {
            "id": 9,
            "vehicle_id": 5,
            "is_active": True,
            "plate": "MNB0989",
            "assign_date": "2022-09-03T19:50:00Z",
            "dismiss_date": None,
        },
    ]
