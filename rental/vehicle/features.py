from .models import Vehicle
from rental.user.models import User
from auditlog.context import set_actor
from rental.vehicle.models import VehiclePlate
from settings.utils.exceptions import NotFound404APIException
from rental.shared_functions.functions import poblate_history_list


def get_vehicles(tenant: int):
    return Vehicle.objects.filter(tenant=tenant, is_deleted=False)


def get_vehicle(vehicle_id: int):
    try:
        return Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(f"Vehicle with id {vehicle_id} doesnt exist")


def create_vehicle(
    user: User,
    type: str = None,
    year: int = None,
    make: str = None,
    model: str = None,
    trim: str = None,
    vin: str = None,
    odometer: int = None,
    nickname: str = None,
    spare_tires: int = None,
    extra_fields=None,
    status: str = None,
    plate: str = None,
):
    with set_actor(user):
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
            tenant=user.defaultTenantUser().tenant,
        )

        if plate:
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
    user: User,
):
    try:
        vehicle = Vehicle.objects.get(id=id)
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(f"Vehicle with id {id} doesnt exist")

    with set_actor(user):
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
            if active_plate:
                if plate != active_plate.plate:
                    active_plate.is_active = False
                    active_plate.save()
                    VehiclePlate.objects.create(vehicle=vehicle, plate=plate)
            else:
                VehiclePlate.objects.create(vehicle=vehicle, plate=plate)

        vehicle.full_clean()
        vehicle.save()


def get_vehicle_history(vehicle_id: int):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        raise NotFound404APIException(f"Vehicle with id {vehicle_id} doesnt exist")

    history_data = []
    plates_logs = []
    pictures_logs = []

    plates = vehicle.plates.all()
    pictures = vehicle.vehicle_pictures.all()

    vehicle_logs = list(vehicle.history.all())
    poblate_history_list(history_data, vehicle_logs, "vehicle")

    for plate in plates:
        plates_logs.extend(plate.history.all())
    poblate_history_list(history_data, plates_logs, "plate")

    for picture in pictures:
        pictures_logs.extend(picture.history.all())
    poblate_history_list(history_data, pictures_logs, "picture")

    return history_data
