# pylint: disable=no-member
from rental.contract_form.models import ContractFormTemplate
import datetime


def get_contract_form_templates(tenant):
    """
    Get all contract form templates
    """
    return ContractFormTemplate.objects.filter(tenant=tenant)
