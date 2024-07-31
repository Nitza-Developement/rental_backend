# pylint: disable=no-member
from rental.contract_form.models import (
    ContractFormTemplate,
    ContractFormField,
    ContractForm,
)
from settings.utils.exceptions import NotFound404APIException


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

    # TODO: hacer que la fecha se la misma que la del original

    form.is_active = False
    form.save()

    form.pk = None
    form._state.adding = True
    form.is_active = True
    form.save()

    return form


def update_contract_form_template(instance, fields=None, **data):
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
