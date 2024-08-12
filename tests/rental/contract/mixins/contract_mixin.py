from datetime import datetime
from typing import Dict, Optional

from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from faker import Faker

from rental.client.models import Client
from rental.contract.features import create_stage_update
from rental.contract.models import Contract, StageUpdate
from rental.rentalPlan.models import RentalPlan
from rental.vehicle.models import Vehicle, VehiclePlate
from tests.util.date_treatment import get_datetime_str_form_in_proper_area

fake = Faker()

User = get_user_model()


class ContractMixin:
    def create_contract(
        self,
        user: User,
        client: Client,
        vehicle: Vehicle,
        rental_plan: RentalPlan,
        active_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Contract:
        with set_actor(user):
            contract = Contract.objects.create(
                tenant=user.defaultTenantUser().tenant,
                client=client,
                vehicle=vehicle,
                rental_plan=rental_plan,
                active_date=active_date,
                end_date=end_date,
            )
            create_stage_update(contract=contract)
            return contract

    def validate_contract_in_list(
        self,
        data: Dict,
        contract_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
    ):
        if not contract_id:
            self.assertEqual(True, "id" in data)
            contract_id = data["id"]
        if not tenant_id:
            self.assertEqual(True, "tenant" in data)
            tenant_id = data["tenant"]
        contract: Contract = Contract.objects.filter(id=contract_id).first()
        self.assertIsNotNone(Contract)

        client: Client = contract.client
        vehicle: Vehicle = contract.vehicle
        plate: VehiclePlate = VehiclePlate.objects.filter(
            vehicle=vehicle
        ).first()
        rental_plan: RentalPlan = contract.rental_plan
        stage_0: StageUpdate = StageUpdate.objects.filter(
            contract=contract
        ).first()

        self.assertDictEqual(
            data,
            {
                "id": contract_id,
                "tenant": tenant_id,
                "client": {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone_number": client.phone_number,
                    "tenant": tenant_id,
                },
                "vehicle": {
                    "id": vehicle.id,
                    "vin": vehicle.vin,
                    "nickname": vehicle.nickname,
                    "odometer": vehicle.odometer,
                    "spare_tires": vehicle.spare_tires,
                    "plate": {
                        "id": plate.id,
                        "plate": plate.plate,
                        "assign_date": get_datetime_str_form_in_proper_area(
                            plate.assign_date
                        ),
                    },
                    "type": vehicle.type,
                    "year": vehicle.year,
                    "make": vehicle.make,
                    "model": vehicle.model,
                    "trim": vehicle.trim,
                    "status": vehicle.status,
                    "tracker": None,
                    "extra_fields": {},
                },
                "rental_plan": {
                    "id": rental_plan.id,
                    "name": rental_plan.name,
                    "amount": rental_plan.amount,
                    "periodicity": rental_plan.periodicity,
                },
                "stages_updates": [
                    {
                        "id": stage.id,
                        "date": get_datetime_str_form_in_proper_area(
                            stage.date
                        ),
                        "reason": stage.reason,
                        "comments": stage.comments,
                        "stage": stage.stage,
                    }
                    for stage in contract.stages_updates.all()
                ],
                "creation_date": get_datetime_str_form_in_proper_area(
                    contract.creation_date
                ),
                "active_date": None,
                "end_date": None,
                "stage": {
                    "reason": stage_0.reason,
                    "comments": stage_0.comments,
                    "stage": stage_0.stage,
                },
                "notes": [
                    {
                        "id": note.id,
                        "contract": note.contract_id,
                        "user": note.user_id,
                        "subject": note.subject,
                        "body": note.body,
                        "createdDate": get_datetime_str_form_in_proper_area(
                            note.createdDate
                        ),
                        "remainder": get_datetime_str_form_in_proper_area(
                            note.remainder
                        ),
                        "file": None,
                    }
                    for note in contract.notes.all()
                ],
                "toll_dues": [
                    {
                        "id": toll_due.id,
                        "amount": toll_due.amount,
                        "plate": toll_due.plate.id,
                        "contract": toll_due.contract_id,
                        "stage": toll_due.stage,
                        "invoice": toll_due.invoice,
                        "invoiceNumber": toll_due.invoiceNumber,
                        "createDate": get_datetime_str_form_in_proper_area(
                            toll_due.createDate
                        ),
                        "note": toll_due.note,
                    }
                    for toll_due in contract.toll_dues.all()
                ],
            },
        )
