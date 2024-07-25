# pylint: disable=no-member
from rental.contract_form.models import ContractFormTemplate


def get_contract_form_templates(tenant):
    """
    Get all contract form templates
    """
    return ContractFormTemplate.objects.filter(tenant=tenant)


def create_contract_form_template(tenant, user, template, name):
    """
    Create a contract form template
    """
    return ContractFormTemplate.objects.create(
        tenant=tenant,
        user=user,
        template=template,
        name=name,
    )
