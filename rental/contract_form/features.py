# pylint: disable=no-member
from rental.contract_form.models import ContractFormTemplate
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


def update_contract_form_template(instance, **data):
    """
    Update a contract form template
    """
    ContractFormTemplate.objects.filter(id=instance.id).update(**data)

    return ContractFormTemplate.objects.get(id=instance.id)
