from django.core.validators import validate_email
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import magic
from rental.forms.models import Field
from rental.inspections.models import Inspection


def validate_inspection_response(data: dict, tenant):

    validate_inspection(data.pop("inspection"), tenant)

    for key in data.keys():
        field = validate_field(key)
        validate_field_value(field, data[key])


def validate_inspection(id, tenant):

    try:
        return Inspection.objects.get(id=id, tenant=tenant)
    except Inspection.DoesNotExist:
        raise ValueError("Inspection does not exist")


def validate_field(id: str):

    if not id.isnumeric():
        raise ValueError(f"Field {id} does not exist")

    try:
        return Field.objects.get(id=id)
    except Field.DoesNotExist:
        raise ValueError(f"Field {id} does not exist")


def validate_field_value(field: Field, value):

    if field.type in (Field.TEXT, Field.DATE, Field.TIME, Field.PHONE):
        if not isinstance(value, str):
            raise ValueError(f"Field {field.id} must be a string")

    elif field.type in (Field.NUMBER, Field.SINGLE_CHECK):
        if not value.isnumeric():
            raise ValueError(f"Field {field.id} must be a number")

    elif field.type == Field.EMAIL:
        try:
            validate_email(value)
        except:
            raise ValueError(f"Field {field.id} must be a valid email")

    elif field.type in (Field.IMAGE, Field.SIGNATURE):

        if not isinstance(value, (InMemoryUploadedFile, TemporaryUploadedFile)):
            raise ValueError(f"Field {field.id} must be an image")

        filetype = magic.from_buffer(value.read(), mime=True)

        if filetype not in ("image/jpeg", "image/jpg", "image/png", "image/webp"):
            raise ValueError(f"Field {field.id} must be a valid image")

        if value.size > 1024 * 1024 * 3:  # 3MB
            raise ValueError(f"Field {field.id} must be less than 3MB")
