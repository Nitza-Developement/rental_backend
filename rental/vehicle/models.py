from datetime import datetime
from django.db import models
from rental.tenant.models import Tenant


def get_image_path(vehiclePicture, picture_filename: str):

    image_extension = picture_filename.split('.')[-1]

    return f'tenant/{vehiclePicture.vehicle.tenant.id}/vehicle/{vehiclePicture.vehicle}/image.{image_extension}'


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
        (ATV, 'ATV'),
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

    type = models.CharField(choices=TYPE_CHOICES)
    year = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    trim = models.CharField(max_length=255)
    vin = models.CharField(max_length=17, unique=True)
    odometer = models.IntegerField()
    nickname = models.CharField(max_length=255)
    spare_tires = models.IntegerField(default=0)
    extra_fields = models.JSONField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name='vehicles')

    def __str__(self) -> str:
        return f'{self.vin} | {self.nickname} | {self.type}'


class VehiclePlate(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.DO_NOTHING, related_name='plates')
    is_active = models.BooleanField(default=True)
    plate = models.CharField(max_length=255, unique=True)
    assign_date = models.DateTimeField(auto_now_add=True)
    dismiss_date = models.DateTimeField(null=True, blank=True)

    def get_active_plate(self):
        return self.plates.filter(is_active=True).first()

    Vehicle.add_to_class('active_plate', get_active_plate)

    def __str__(self) -> str:
        return f'{self.plate}'

    def save(self, *args, **kwargs):
        if self.pk is None or self.is_active != True:
            if not self.is_active:
                self.dismiss_date = datetime.now()
        super().save(*args, **kwargs)


class VehiclePicture(models.Model):
    image = models.ImageField(upload_to=get_image_path, null=False, blank=False)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='vehicle_pictures')
    pinned = models.BooleanField(default=False)
