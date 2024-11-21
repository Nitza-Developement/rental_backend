# pylint: disable=no-member
from rental.contract_form.models import (
    ContractFormTemplate,
    ContractFormField,
    ContractForm,
    ContractFormFieldResponse,
)
from settings.utils.exceptions import NotFound404APIException

from settings.settings import MINIO_STORAGE_MEDIA_BUCKET_NAME
from settings.utils.minio_client import minio_client


def get_contract_form_templates(tenant):
    """
    Get all contract form templates
    """
    return ContractFormTemplate.objects.filter(tenant=tenant, is_active=True)


def create_contract_form_template(**data):
    """
    Create a contract form template
    """
    return ContractFormTemplate.objects.create(**data)


def get_contract_form_template(tenant, id):
    """
    Get a contract form template
    """
    try:
        return ContractFormTemplate.objects.get(tenant=tenant, id=id, is_active=True)
    except ContractFormTemplate.DoesNotExist as error:
        raise NotFound404APIException(
            f"Contract form template with ID {id} doesnt exists"
        ) from error


def delete_contract_form_template(tenant, id):
    """
    Delete a contract form template
    """
    form = get_contract_form_template(tenant, id)
    if form:
        form.is_active = False
        form.save()


def clone_contract_form_template(form: ContractFormTemplate):
    """
    Clone a contract form template
    """

    form.is_active = False
    form.save()

    fields = ContractFormField.objects.filter(template=form).all()

    form.pk = None
    form._state.adding = True
    form.is_active = True
    form.save()

    for field in fields:
        field.pk = None
        field._state.adding = True
        field.template = form
        field.save()

    return form


def update_contract_form_template(instance: ContractFormTemplate, fields=None, **data):
    """
    Update a contract form template
    """
    ContractFormTemplate.objects.filter(id=instance.id).update(**data)

    if fields:

        ContractFormField.objects.filter(template=instance).delete()

        ContractFormField.objects.bulk_create(
            [
                ContractFormField(
                    template=instance,
                    placeholder=field.get("placeholder"),
                    type=field.get("type"),
                )
                for field in fields
            ]
        )

    return ContractFormTemplate.objects.get(id=instance.id)


def get_contract_forms(tenant):
    """
    Get all contract form
    """
    return ContractForm.objects.filter(tenant=tenant)


def create_contract_form(**data):
    """
    Create a contract form
    """

    return ContractForm.objects.create(**data)


def get_contract_form(tenant, id):
    """
    Get a contract form
    """
    try:
        return ContractForm.objects.get(tenant=tenant, id=id)
    except ContractForm.DoesNotExist as error:
        raise NotFound404APIException(
            f"Contract form with ID {id} doesnt exists"
        ) from error


def create_contract_form_response(tenant, data):
    """Create response to contract form"""

    contract_form = get_contract_form(tenant, data.get("contract_form"))
    fields = ContractFormField.objects.filter(template=contract_form.template).all()

    for field in fields:

        if field.type in (
            ContractFormField.TEXT,
            ContractFormField.PHONE,
            ContractFormField.NUMBER,
            ContractFormField.EMAIL,
        ):

            ContractFormFieldResponse.objects.create(
                form=contract_form, field=field, content=data.get(f"{field.id}")
            )

        elif field.type == ContractFormField.SIGNATURE:
            file = data.get(f"{field.id}")
            file.seek(0)

            length_file = len(file.file.getvalue())

            file_name = f"contract-signature-{field.id}.png"

            result = minio_client().put_object(
                bucket_name=MINIO_STORAGE_MEDIA_BUCKET_NAME,
                object_name=f"contract_form/{contract_form.id}/{file_name}",
                data=file,
                length=length_file,
            )

            ContractFormFieldResponse.objects.create(
                form=contract_form, field=field, content=result.object_name
            )

    return contract_form
