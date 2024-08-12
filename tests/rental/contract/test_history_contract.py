from datetime import datetime
from typing import Any, Dict, Optional

from auditlog.context import set_actor
from auditlog.models import LogEntry
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from rental.client.models import Client
from rental.contract.models import Contract
from rental.rentalPlan.models import RentalPlan
from rental.vehicle.models import Vehicle, VehiclePlate
from tests.rental.contract.parent_case.contract_api_test_case import (
    ContractApiTestCase,
)

fake = Faker()
User = get_user_model()


class TestHistoryContract(ContractApiTestCase):
    def setUp(self):
        super().setUp()
        self.user_contract = self.create_tenant_user().default_tenant_user.user
        self.list_contract = [
            self.create_contract(
                user=self.user_contract,
                client=self.create_client(user=self.user_contract),
                vehicle=self.create_vehicle(user=self.user_contract),
                rental_plan=self.create_rental_plan(user=self.user_contract),
            )
            for _ in range(2)
        ]
        for i in range(2):
            contract: Contract = self.list_contract[i]
            for j in range(3):
                self.create_note(user=self.user_contract, contract=contract)
                self.create_toll_due(
                    user=self.user_contract,
                    contract=contract,
                    plate=VehiclePlate.objects.filter(
                        vehicle=contract.vehicle
                    ).first(),
                )
        self.maxDiff = None
        for _ in range(3):
            for i in range(len(self.list_contract)):
                self.list_contract[i] = self.custom_update_contract(
                    contract=self.list_contract[i],
                    user=self.user_contract,
                    client=self.create_client(user=self.user_contract),
                    vehicle=self.create_vehicle(user=self.user_contract),
                    rental_plan=self.create_rental_plan(
                        user=self.user_contract
                    ),
                )

    def custom_update_contract(
        self,
        contract: Contract,
        user: User,
        client: Client,
        vehicle: Vehicle,
        rental_plan: RentalPlan,
        active_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Contract:
        with set_actor(user):
            contract.vehicle = vehicle
            contract.rental_plan = rental_plan
            contract.active_date = active_date
            contract.end_date = end_date
            contract.client = client
            contract.save()
            return contract

    def call_history_contract(
        self,
        entity_id: int,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        URL = reverse("contract-actions-history", args=[entity_id])
        response_dict = self.call_retrieve(
            url=URL,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        self.assertTrue(True, isinstance(response_dict, list))
        for history in response_dict:
            self.validate_history_contract(data=history)

        return response_dict

    def validate_history_contract(self, data: Dict[str, Any]):
        action = self.assertKey(
            data,
            "action",
            expected_any=[
                LogEntry.Action.CREATE,
                LogEntry.Action.UPDATE,
                LogEntry.Action.DELETE,
                LogEntry.Action.ACCESS,
            ],
        )
        model = self.assertKey(
            data,
            "model",
            expected_any=[
                "contract",
                "stage_update",
                "note",
                "rental_plan",
                "toll_due",
            ],
        )
        changes = self.assertKey(data, "changes", expected_type=dict)

        if model == "contract":
            list_keys_changes = [
                "tenant",
                "client",
                "vehicle",
                "rental plan",
                "creation date",
                "active_date",
                "notes",
                "toll_dues",
                "stages_updates",
            ]
        elif model == "stage_update":
            list_keys_changes = [
                "date",
                "reason",
                "comments",
                "stage",
                "contract",
            ]
        elif model == "note":
            list_keys_changes = [
                "contract",
                "user",
                "subject",
                "body",
                "createdDate",
                "remainder",
                "file",
            ]
        elif model == "rental_plan":
            list_keys_changes = [
                "name",
                "amount",
                "periodicity",
                "tenant",
                "contracts",
            ]
        elif model == "toll_due":
            list_keys_changes = [
                "amount",
                "plate",
                "contract",
                "stage",
                "invoice",
                "invoiceNumber",
                "createDate",
                "note",
            ]
        if action == LogEntry.Action.CREATE:
            list_keys_changes += ["ID"]

        for key in changes:
            # print(model)
            # print(changes)
            self.assertIn(key, list_keys_changes)
            self.assertKey(changes, key, expected_in_list_of_type=[str, str])
        self.assertKey(data, "timestamp", expected_none=False)
        user = self.user_contract
        self.assertKey(
            data,
            "actor",
            expected_dict={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": None,
            },
        )

    def test_history_contract(self):
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        for entity in self.list_contract:
            # case correct, response 200
            self.call_history_contract(
                entity_id=entity.id, print_json_response=False
            )
