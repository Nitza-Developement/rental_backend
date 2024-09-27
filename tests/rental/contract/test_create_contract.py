from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from rental.client.models import Client
from rental.contract.models import Contract, StageUpdate
from rental.rentalPlan.models import RentalPlan
from rental.vehicle.models import Vehicle, VehiclePlate
from tests.rental.contract.parent_case.contract_api_test_case import (
    ContractApiTestCase,
)
from tests.util.date_treatment import get_datetime_str_form_in_proper_area

fake = Faker()
User = get_user_model()


class TestCreateContract(ContractApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = self.custom_staff.user
        self.client_entity = self.create_client(user=user)
        self.rental_plan = self.create_rental_plan(user=user)
        self.vehicle = self.create_vehicle(user=user)
        self.maxDiff = None

    def call_create_contract(
        self,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ):
        URL = reverse("contract")

        payload = {
            "client": self.client_entity.id,
            "vehicle": self.vehicle.id,
            "rental_plan": self.rental_plan.id,
        }

        return self.call_create(
            url=URL,
            payload=payload,
            unauthorized=unauthorized,
            forbidden=forbidden,
            bad_request=bad_request,
            print_json_response=print_json_response,
        )

    def test_create_contract(self):
        initial_amount = Contract.objects.count()

        # case not authenticated, response 401
        self.call_create_contract(
            unauthorized=True,
        )
        self.assertEqual(initial_amount, Contract.objects.count())

        # case bad authenticated user (not admin), response 403
        self.login(custom_user=self.custom_user)
        self.put_authentication_in_the_header()
        self.call_create_contract(
            forbidden=True,
        )
        self.assertEqual(initial_amount, Contract.objects.count())

        # case correct, response 201
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        response_dict = self.call_create_contract(
            print_json_response=False,
        )
        self.assertEqual(initial_amount + 1, Contract.objects.count())
        self.assertEqual(True, "id" in response_dict)
        contract_id = response_dict["id"]
        contract: Contract = Contract.objects.filter(id=contract_id).first()
        self.assertIsNotNone(contract)
        tenant_id = self.custom_staff.user.defaultTenantUser().tenant.id
        client: Client = self.client_entity
        vehicle: Vehicle = self.vehicle
        plate: VehiclePlate = VehiclePlate.objects.filter(
            vehicle=vehicle
        ).first()
        rental_plan: RentalPlan = self.rental_plan
        stage: StageUpdate = StageUpdate.objects.filter(
            contract=contract
        ).first()
        self.assertEqual(1, StageUpdate.objects.count())
        self.assertDictEqual(
            response_dict,
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
                        "reason": None,
                        "comments": None,
                        "stage": "Pending",
                    }
                ],
                "creation_date": get_datetime_str_form_in_proper_area(
                    contract.creation_date
                ),
                "active_date": None,
                "end_date": None,
                "stage": {"reason": None, "comments": None, "stage": "Pending"},
                "notes": [],
                "toll_dues": [],
            },
        )
