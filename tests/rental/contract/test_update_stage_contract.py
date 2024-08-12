import random
from typing import Optional

from django.urls import reverse
from faker import Faker

from rental.contract.models import Contract, StageUpdate
from rental.vehicle.models import VehiclePlate
from tests.rental.contract.parent_case.contract_api_test_case import (
    ContractApiTestCase,
)

fake = Faker()


class TestUpdateStageContract(ContractApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user

        self.list_contract = [
            self.create_contract(
                user=user,
                client=self.create_client(user=user),
                vehicle=self.create_vehicle(user=user),
                rental_plan=self.create_rental_plan(user=user),
            )
            for _ in range(2)
        ]
        for i in range(2):
            contract: Contract = self.list_contract[i]
            for j in range(3):
                self.create_note(user=user, contract=contract)
                self.create_toll_due(
                    user=user,
                    contract=contract,
                    plate=VehiclePlate.objects.filter(
                        vehicle=contract.vehicle
                    ).first(),
                )
        self.maxDiff = None

    def call_update_contract(
        self,
        entity_id: int,
        reason: Optional[str] = None,
        comments: Optional[str] = None,
        stage: Optional[str] = None,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("contract-actions", args=[entity_id])
        # print(URL)
        if not reason:
            reason = fake.text(max_nb_chars=30)
        if not comments:
            comments = fake.text(max_nb_chars=30)
        if not stage:
            stage = random.choices(
                [
                    StageUpdate.ACTIVE,
                    StageUpdate.PENDING,
                    StageUpdate.DISMISS,
                    StageUpdate.ENDED,
                ]
            )
        payload = {"reason": reason, "comments": comments, "stage": stage}
        response_dict = self.call_partial_update(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            not_found=not_found,
            print_json_response=print_json_response,
        )
        if response_dict:
            self.validate_contract_in_list(
                data=response_dict,
                contract_id=entity_id,
            )
        return response_dict

    def test_update_stage_contract(self):
        initial_amount_contract = Contract.objects.count()
        initial_amount_stage = StageUpdate.objects.count()
        contract = self.list_contract[0]

        # case not authenticated, response 401
        self.call_update_contract(
            entity_id=contract.id,
            reason="fake reason",
            comments="fake comments",
            stage=StageUpdate.ENDED,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())
        self.assertEqual(initial_amount_stage, StageUpdate.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_update_contract(
            entity_id=contract.id,
            reason="fake reason",
            comments="fake comments",
            stage=StageUpdate.ENDED,
            unauthorized=True,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())
        self.assertEqual(initial_amount_stage, StageUpdate.objects.count())

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_contract(
            entity_id=999999,
            reason="fake reason",
            comments="fake comments",
            stage=StageUpdate.ENDED,
            not_found=True,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())
        self.assertEqual(initial_amount_stage, StageUpdate.objects.count())

        # case correct, response 200
        self.call_update_contract(
            entity_id=contract.id,
            reason="fake reason",
            comments="fake comments",
            stage=StageUpdate.ENDED,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())
        self.assertEqual(initial_amount_stage + 1, StageUpdate.objects.count())
