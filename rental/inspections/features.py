from rental.inspections.models import Inspection
from django.core.files.uploadedfile import InMemoryUploadedFile
from rental.forms.models import FieldResponse, Field, CheckOption
from settings.utils.exceptions import NotFound404APIException
from minio import Minio
from settings.settings import (
    MINIO_STORAGE_ACCESS_KEY,
    MINIO_STORAGE_SECRET_KEY,
    MINIO_STORAGE_ENDPOINT,
    MINIO_STORAGE_USE_HTTPS,
    MINIO_STORAGE_MEDIA_BUCKET_NAME,
)


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

    inspection = get_inspection(data.pop("inspection"), tenant)

    client = Minio(
        endpoint=MINIO_STORAGE_ENDPOINT,
        access_key=MINIO_STORAGE_ACCESS_KEY,
        secret_key=MINIO_STORAGE_SECRET_KEY,
        secure=MINIO_STORAGE_USE_HTTPS,
    )

    found = client.bucket_exists(MINIO_STORAGE_MEDIA_BUCKET_NAME)
    if not found:
        client.make_bucket(MINIO_STORAGE_MEDIA_BUCKET_NAME)

    for field_id in data.keys():

        # :note is used in the keys to identify
        # that it is a note of the check option
        if ":note" in field_id:
            continue

        response = data[field_id]

        field = Field.objects.get(id=field_id)

        if field.type in (
            Field.TEXT,
            Field.NUMBER,
            Field.DATE,
            Field.TIME,
            Field.PHONE,
            Field.EMAIL,
        ):
            FieldResponse.objects.create(
                field=field,
                tenantUser=tenantUser,
                inspection=inspection,
                content=response,
            )

        elif field.type == Field.SINGLE_CHECK:

            check_option = CheckOption.objects.get(id=response)

            FieldResponse.objects.create(
                field=field,
                tenantUser=tenantUser,
                inspection=inspection,
                check_option=check_option,
                note=data.get(f"{field_id}:note"),
            )

        elif field.type in (Field.SIGNATURE, Field.IMAGE):

            file = response.file
            # Restablece la posición del puntero al inicio del búfer
            file.seek(0)

            length_file = len(response.file.getvalue())

            if field.type == Field.SIGNATURE:
                file_name = f"signature-{field.id}.png"
            else:
                file_name = f"image-{field.id}.png"

            result = client.put_object(
                bucket_name=MINIO_STORAGE_MEDIA_BUCKET_NAME,
                object_name=f"/inspections/{inspection.id}/{file_name}",
                data=file,
                length=length_file,
            )

            FieldResponse.objects.create(
                field=field,
                tenantUser=tenantUser,
                inspection=inspection,
                content=result.object_name,
            )

    return inspection
