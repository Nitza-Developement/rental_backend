from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.vehicle.models import Vehicle, VehiclePicture


@SeederRegistry.register
class VehiclePictureSeeder(seeders.ModelSeeder):
    id = "VehiclePictureSeeder"
    priority = 6
    model = VehiclePicture
    vehicles = Vehicle.objects.all()
    data = [
        {
            "vehicle": vehicles[0],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[1],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[2],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[3],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[4],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[5],
            "image": "sample1",
            "pinned": True,
        },
        {
            "vehicle": vehicles[6],
            "image": "sample1",
            "pinned": True,
        },
    ]
