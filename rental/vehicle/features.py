from .models import Vehicle
from django.db.models import Q
from rental.vehicle.models import VehiclePlate

from settings.utils.exceptions import NotFound404APIException


def get_vehicles(tenant: int):
    return Vehicle.objects.filter(tenant=tenant, is_deleted = False)


def get_vehicle(search_by: int | str = None):
    try:
        return Vehicle.objects.filter(
            Q(id=search_by) | Q(vin__icontains=search_by)
        ).first()
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(
            f"Vehicle with id or vin {search_by} doesnt exist"
        )


def create_vehicle(
    type: str,
    year: int,
    make: str,
    model: str,
    trim: str,
    vin: str,
    odometer: int,
    nickname: str,
    spare_tires: int,
    extra_fields,
    status: str,
    plate: str,
    tenant: int,
):

    new_vehicle = Vehicle.objects.create(
        type=type,
        year=year,
        make=make,
        model=model,
        trim=trim,
        vin=vin,
        odometer=odometer,
        nickname=nickname,
        spare_tires=spare_tires,
        extra_fields=extra_fields,
        status=status,
        tenant=tenant,
    )

    VehiclePlate.objects.create(vehicle=new_vehicle, plate=plate)

    return new_vehicle


def delete_vehicle(vehicle_id: int):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle.is_deleted = True
        vehicle.save()
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(f"Vehicle doesnt exist")


def update_vehicle(
    id: int,
    type: str,
    year: int,
    make: str,
    model: str,
    trim: str,
    vin: str,
    odometer: int,
    nickname: str,
    spare_tires: int,
    extra_fields,
    status: str,
    plate: str,
):
    try:
        vehicle = Vehicle.objects.get(id=id)
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(f"Vehicle with id {id} doesnt exist")

    if type:
        vehicle.type = type

    if year:
        vehicle.year = year

    if make:
        vehicle.make = make

    if model:
        vehicle.model = model

    if trim:
        vehicle.trim = trim

    if vin:
        vehicle.vin = vin

    if odometer:
        vehicle.odometer = odometer

    if nickname:
        vehicle.nickname = nickname

    if spare_tires:
        vehicle.spare_tires = spare_tires

    if extra_fields:
        vehicle.extra_fields = extra_fields

    if status:
        vehicle.status = status

    if plate:
        active_plate = vehicle.active_plate()
        if plate != active_plate.plate:
            active_plate.is_active = False
            active_plate.save()
            VehiclePlate.objects.create(vehicle=vehicle, plate=plate)

    vehicle.full_clean()
    vehicle.save()
