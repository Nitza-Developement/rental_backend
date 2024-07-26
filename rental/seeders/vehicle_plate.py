from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.vehicle.models import Vehicle, VehiclePlate


@SeederRegistry.register
class VehiclePlateSeeder(seeders.ModelSeeder):
    id = "VehiclePlateSeeder"
    priority = 5
    model = VehiclePlate
    vehicles = Vehicle.objects.all()
    data = [
        {
            "vehicle": vehicles[0],
            "is_active": True,
            "plate": "ABC1234",
            "assign_date": "2023-06-01T08:30:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[1],
            "is_active": True,
            "plate": "XYZ5678",
            "assign_date": "2022-08-15T09:45:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[2],
            "is_active": True,
            "plate": "LMN4321",
            "assign_date": "2021-12-05T07:20:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[3],
            "is_active": True,
            "plate": "QWE9876",
            "assign_date": "2020-10-11T11:10:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[4],
            "is_active": False,
            "plate": "ASD5432",
            "assign_date": "2019-07-23T13:30:00Z",
            "dismiss_date": "2022-09-01T14:00:00Z",
        },
        {
            "vehicle": vehicles[5],
            "is_active": True,
            "plate": "ASD5439",
            "assign_date": "2022-09-01T20:00:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[6],
            "is_active": True,
            "plate": "JKL3210",
            "assign_date": "2023-02-27T16:15:00Z",
            "dismiss_date": None,
        },
        {
            "vehicle": vehicles[2],
            "is_active": False,
            "plate": "MNB0987",
            "assign_date": "2018-04-14T10:05:00Z",
            "dismiss_date": "2021-11-30T09:50:00Z",
        },
        {
            "vehicle": vehicles[4],
            "is_active": True,
            "plate": "MNB0989",
            "assign_date": "2022-09-03T19:50:00Z",
            "dismiss_date": None,
        },
    ]
