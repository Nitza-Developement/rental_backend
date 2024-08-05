from django.core.validators import validate_email
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import magic
from rental.contract_form.models import ContractForm, ContractFormField


def validate_contract_form_response(tenant, data: dict):

    keys = data.keys()

    if "contract_form" not in keys:
        raise ValueError(f"Set contract form")

    contract_form = validate_contract_form(data.get("contract_form"), tenant)
    fields = ContractFormField.objects.filter(template=contract_form.template).all()

    for field in fields:

        if field.required and str(field.id) not in keys:
            raise ValueError(f"Field {field.id} is required")

        validate_field_value(field, data.get(f"{field.id}"))


def validate_field_value(field: ContractFormField, value):
    """Validate the value from field"""

    if field.type in (ContractFormField.TEXT, ContractFormField.PHONE):
        if not isinstance(value, str):
            raise ValueError(f"Field {field.id} must be a string")

    elif field.type == ContractFormField.NUMBER:
        if not value.isnumeric():
            raise ValueError(f"Field {field.id} must be a number")

    elif field.type == ContractFormField.EMAIL:
        try:
            validate_email(value)
        except Exception as error:
            raise ValueError(f"Field {field.id} must be a valid email") from error

    elif field.type == ContractFormField.SIGNATURE:

        if not isinstance(value, (InMemoryUploadedFile, TemporaryUploadedFile)):
            raise ValueError(f"Field {field.id} must be an image")

        filetype = magic.from_buffer(value.read(), mime=True)

        if filetype not in ("image/jpeg", "image/jpg", "image/png", "image/webp"):
            raise ValueError(f"Field {field.id} must be a valid image")

        if value.size > 1024 * 1024 * 3:  # 3MB
            raise ValueError(f"Field {field.id} must be less than 3MB")


def validate_contract_form(id: int, tenant):
    """Return instance of ContractForm or raise ValueError"""

    try:
        return ContractForm.objects.get(id=id, tenant=tenant)
    except ContractForm.DoesNotExist as error:
        raise ValueError("Contract form does not exist") from error
