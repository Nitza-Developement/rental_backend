from rental.inspections.models import Inspection
from settings.utils.exceptions import NotFound404APIException


def get_inspection(inspection_id, tenant):
    try:
        return Inspection.objects.get(id=inspection_id, tenant=tenant)
    except Inspection.DoesNotExist:
        raise NotFound404APIException(f"Form with ID {inspection_id} doesnt exists")


def get_inspections(tenant):
    inspections = Inspection.objects.filter(tenant=tenant).all()
    return inspections


def create_inspection(form, vehicle, tenant, tenantUser):

    return Inspection.objects.create(
        form=form,
        vehicle=vehicle,
        tenant=tenant,
        tenantUser=tenantUser,
    )
