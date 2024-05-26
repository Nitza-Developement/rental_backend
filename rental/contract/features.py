from rental.contract.models import Contract, StageUpdate
from settings.utils.exceptions import NotFound404APIException


def create_stage_update(
    date=None, reason=None, comments=None, stage="Pending", contract=None
):
    stage_update = StageUpdate.objects.create(
        date=date, reason=reason, comments=comments, stage=stage, contract=contract
    )
    return stage_update


def create_contract(
    tenant, client, vehicle, rental_plan, active_date=None, end_date=None
):
    contract = Contract.objects.create(
        tenant=tenant,
        client=client,
        vehicle=vehicle,
        rental_plan=rental_plan,
        active_date=active_date,
        end_date=end_date,
    )
    return contract


def get_contracts(tenant):
    return Contract.objects.filter(tenant=tenant)


def get_contract(contract_id):
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        raise NotFound404APIException(f"Contract with id {contract_id} not found")
    return contract


def update_contract(contract_id, client=None, vehicle=None, rental_plan=None):
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        raise NotFound404APIException(f"Contract with id {contract_id} not found")

    if client:
        contract.client = client
    if vehicle:
        contract.vehicle = vehicle
    if rental_plan:
        contract.rental_plan = rental_plan

    contract.save()
    return contract
