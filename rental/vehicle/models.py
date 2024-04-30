from django.db import models
from django.contrib.postgres.fields import JSONField


class Vehicle(models.Model):
    ATV = 'ATV'
    BOAT = 'Boat'
    BUS = 'Bus'
    CAR = 'Car'
    CHASIS = 'Chassis'
    EQUIPMENT = 'Equipment'
    FORKLIFT = 'Forklift'
    FREIGHTLINER = 'Freightliner'
    GENERATOR = 'Generator'
    MACHINERY = 'Machinery'
    MOTORCYCLE = 'Motorcycle'
    PLANE = 'Plane'
    RV = 'RV'
    SUV = 'SUV'
    TRACTOR = 'Tractor'
    TRAILER = 'Trailer'
    TRUCK = 'Truck'
    VAN = 'Van'
    CUSTOM = 'Custom'
    AVAILABLE = 'Available'
    UNAVAILABLE = 'Unavailable'

    TYPE_CHOICES = [
        (ATV, 'All Terrain Vehicle'),
        (BOAT, 'Boat'),
        (BUS, 'Bus'),
        (CAR, 'Car'),
        (CHASIS, 'Chassis'),
        (EQUIPMENT, 'Equipment'),
        (FORKLIFT, 'Forklift'),
        (FREIGHTLINER, 'Freightliner'),
        (GENERATOR, 'Generator'),
        (MACHINERY, 'Machinery'),
        (MOTORCYCLE, 'Motorcycle'),
        (PLANE, 'Plane'),
        (RV, 'Recreational Vehicle'),
        (SUV, 'Sport Utility Vehicle'),
        (TRACTOR, 'Tractor'),
        (TRAILER, 'Trailer'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
        (CUSTOM, 'Custom'),
    ]

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable')
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    trim = models.CharField(max_length=255)
    vin = models.CharField(max_length=17, unique=True)
    odometer = models.IntegerField()
    nickname = models.CharField(max_length=255)
    spare_tires = models.IntegerField(default=0)
    extraFields = JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class VehiclePlate(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='plates')
    isActive = models.BooleanField(default=False)
    plate = models.CharField(max_length=255, unique=True)
    assignDate = models.DateTimeField(auto_now_add=True)
    dismissDate = models.DateTimeField(null=True, blank=True)


class VehiclePicture(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=255)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='vehicle_pictures')
    pinned = models.BooleanField(default=False)
