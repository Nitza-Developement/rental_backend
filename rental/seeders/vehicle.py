from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import Tenant
from rental.vehicle.models import Vehicle

tenant = Tenant.objects.first()


@SeederRegistry.register
class VehicleSeeder(seeders.ModelSeeder):
    id = "VehicleSeeder"
    priority = 4
    model = Vehicle
    data = [
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
        {
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
            "tenant": tenant,
        },
    ]
