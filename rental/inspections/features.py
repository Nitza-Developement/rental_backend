from rental.inspections.models import Inspection
from rental.forms.models import Form
from rental.models import Vehicle


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
