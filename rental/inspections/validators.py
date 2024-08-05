from django.core.validators import validate_email
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import magic
from rental.forms.models import Field, Card
from rental.inspections.models import Inspection


def validate_inspection_response(data: dict, tenant):

    inspection = validate_inspection(data.pop("inspection"), tenant)
    cards = Card.objects.filter(form__id=inspection.form.id).all()

    fields = sum([list(card.fields.all()) for card in cards], [])

    required_fields = [field.id for field in fields if field.required]
    valid_fields = [field.id for field in fields]

    missing_fields = [
        str(field_id)
        for field_id in required_fields
        if str(field_id) not in data.keys()
    ]

    if missing_fields:
        raise ValueError("Missing fields: {0}".format(",".join(missing_fields)))

    for field_id in data.keys():

        # :note is used in the keys to identify
        # that it is a note of the check option
        if ":note" in field_id:
            if not isinstance(data[field_id], str):
                raise ValueError(f"Field {field_id} must be a string.")
            continue

        if not field_id.isnumeric():
            raise ValueError(f"Field {field_id} does not exist.")

        if int(field_id) not in valid_fields:
            raise ValueError(
                f"Field {field_id} does not exist in this inspection or not exist."
            )

        field = Field.objects.get(id=field_id)
        validate_field_value(field, data[field_id])


def validate_inspection(id, tenant):

    try:
        return Inspection.objects.get(id=id, tenant=tenant)
    except Inspection.DoesNotExist:
        raise ValueError("Inspection does not exist")


def validate_field_value(field: Field, value):

    if field.type in (Field.TEXT, Field.DATE, Field.TIME, Field.PHONE):
        if not isinstance(value, str):
            raise ValueError(f"Field {field.id} must be a string")

    elif field.type == Field.NUMBER:
        if not value.isnumeric():
            raise ValueError(f"Field {field.id} must be a number")

    elif field.type == Field.SINGLE_CHECK:
        valid_options = [option.id for option in field.check_options.all()]

        if not value.isnumeric():
            raise ValueError(f"Field {field.id} must be a number")
        if int(value) not in valid_options:
            raise ValueError(f"Check option {value} does not exist")

    elif field.type == Field.EMAIL:
        try:
            validate_email(value)
        except Exception as error:
            raise ValueError(f"Field {field.id} must be a valid email") from error

    elif field.type in (Field.IMAGE, Field.SIGNATURE):

        if not isinstance(value, (InMemoryUploadedFile, TemporaryUploadedFile)):
            raise ValueError(f"Field {field.id} must be an image")

        filetype = magic.from_buffer(value.read(), mime=True)

        if filetype not in ("image/jpeg", "image/jpg", "image/png", "image/webp"):
            raise ValueError(f"Field {field.id} must be a valid image")

        if value.size > 1024 * 1024 * 3:  # 3MB
            raise ValueError(f"Field {field.id} must be less than 3MB")
