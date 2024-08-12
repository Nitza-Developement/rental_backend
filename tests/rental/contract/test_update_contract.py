from typing import List

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


class TestUpdateContract(ContractApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.create_tenant_user().default_tenant_user.user
        self.vehicles: List[Vehicle] = [
            self.create_vehicle(user=user) for _ in range(3)
        ]
        self.rental_plans: List[RentalPlan] = [
            self.create_rental_plan(user=user) for _ in range(3)
        ]
        self.clients: List[Client] = [
            self.create_client(user=user) for _ in range(3)
        ]
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
        client: Client,
        vehicle: Vehicle,
        rental_plan: RentalPlan,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("contract-actions", args=[entity_id])
        # print(URL)

        payload = {
            "client": client.id,
            "vehicle": vehicle.id,
            "rental_plan": rental_plan.id,
        }
        response_dict = self.call_update(
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

    def test_update_contract(self):
        initial_amount_contract = Contract.objects.count()
        contract = self.list_contract[0]

        # case not authenticated, response 401
        self.call_update_contract(
            entity_id=contract.id,
            vehicle=self.vehicles[0],
            client=self.clients[0],
            rental_plan=self.rental_plans[0],
            unauthorized=True,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())

        # case bad authenticated user (not admin), response 401
        self.login(custom_user=self.custom_user)
        self.call_update_contract(
            entity_id=contract.id,
            vehicle=self.vehicles[0],
            client=self.clients[0],
            rental_plan=self.rental_plans[0],
            unauthorized=True,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())

        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()

        # case not found, response 404
        self.call_update_contract(
            entity_id=999999,
            vehicle=self.vehicles[0],
            client=self.clients[0],
            rental_plan=self.rental_plans[0],
            not_found=True,
            print_json_response=False,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())

        # case correct, response 200
        self.call_update_contract(
            entity_id=contract.id,
            vehicle=self.vehicles[0],
            client=self.clients[0],
            rental_plan=self.rental_plans[0],
            print_json_response=False,
        )
        self.assertEqual(initial_amount_contract, Contract.objects.count())
