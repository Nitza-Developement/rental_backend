from django.db import models
from datetime import datetime
from rental.tenant.models import Tenant
from auditlog.models import AuditlogHistoryField


def get_image_path(vehiclePicture, picture_filename: str):
    return f"tenant/{vehiclePicture.vehicle.tenant.id}/vehicle/{vehiclePicture.vehicle}/{picture_filename}"


class Vehicle(models.Model):
    CAR = "Car"
    FREIGHTLINER = "Freightliner"
    TRAILER = "Trailer"
    TRUCK = "Truck"
    VAN = "Van"
    SUV = "SUV"
    CUSTOM = "Custom"
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    RENTED = "Rented"
    IN_MAINTENANCE = "In Maintenance"

    TYPE_CHOICES = [
        (CAR, "Car"),
        (SUV, "SUV"),
        (FREIGHTLINER, "Freightliner"),
        (TRAILER, "Trailer"),
        (TRUCK, "Truck"),
        (VAN, "Van"),
        (CUSTOM, "Custom"),
    ]

    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (UNAVAILABLE, "Unavailable"),
        (RENTED, "Rented"),
        (IN_MAINTENANCE, "In Maintenance"),
    ]

    type = models.CharField(choices=TYPE_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    trim = models.CharField(max_length=255, null=True, blank=True)
    vin = models.CharField(max_length=17, unique=True)
    odometer = models.IntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    spare_tires = models.IntegerField(default=0, null=True, blank=True)
    extra_fields = models.JSONField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES)
    is_deleted = models.BooleanField(default=False)
    history = AuditlogHistoryField()
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="vehicles"
    )

    def __str__(self) -> str:
        return f"{self.vin} | {self.nickname} | {self.type}"

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["id"]


class VehiclePlate(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.DO_NOTHING, related_name="plates"
    )
    is_active = models.BooleanField(default=True)
    plate = models.CharField(max_length=255, unique=True)
    assign_date = models.DateTimeField(auto_now_add=True)
    dismiss_date = models.DateTimeField(null=True, blank=True)
    history = AuditlogHistoryField()

    def get_active_plate(self):
        return self.plates.filter(is_active=True).first()

    Vehicle.add_to_class("active_plate", get_active_plate)

    def __str__(self) -> str:
        return f"{self.plate}"

    def save(self, *args, **kwargs):
        if self.pk is None or not self.is_active:
            if not self.is_active:
                self.dismiss_date = datetime.now()
        super().save(*args, **kwargs)


class VehiclePicture(models.Model):
    image = models.ImageField(upload_to=get_image_path, null=False, blank=False)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="vehicle_pictures"
    )
    pinned = models.BooleanField(default=False)
    history = AuditlogHistoryField()
