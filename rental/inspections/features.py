from rental.inspections.models import Inspection
from rental.forms.models import FieldResponse, Field
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


def create_inspection_response(data: dict, tenant, tenantUser):
    print(data)

    inspection = get_inspection(data.pop("inspection"), tenant)

    for field_id in data.keys():
        content = data[field_id]

        field = Field.objects.get(id=field_id)


        if field.type in (Field.TEXT, Field.DATE, Field.TIME, Field.PHONE):
            FieldResponse.objects.create(
                field=field,
                tenantUser=tenantUser,
                inspection=inspection,
                content=content

            )


        # FieldResponse.objects.create(

        # )

    print(inspection)

    return inspection
