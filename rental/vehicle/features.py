from .models import Vehicle
from django.db.models import Q
from .models import VehiclePlate

from settings.utils.exceptions import NotFound404APIException


def get_vehicles():
    return Vehicle.objects.all()


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
    vehicle_type: str,
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

    new_vehicle = Vehicle.objects.create(
        vehicle_type=vehicle_type,
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
    )

    VehiclePlate.objects.create(vehicle=new_vehicle, plate=plate)

    return new_vehicle


def delete_vehicle(search_by: int | str):
    try:
        Vehicle.objects.filter(Q(id=search_by) | Q(vin__icontains=search_by)).delete()
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(
            f"Vehicle with id or vin {search_by} doesnt exist"
        )


def update_vehicle(search_by: int | str, plate: str):
    try:
        vehicle = Vehicle.objects.filter(
            Q(id=search_by) | Q(vin__icontains=search_by)
        ).first()
        active_plate = vehicle.active_plate()
        active_plate.is_active = False
        active_plate.save()
        VehiclePlate.objects.create(vehicle=vehicle, plate=plate)
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(
            f"Vehicle with id or vin {search_by} doesnt exist"
        )
