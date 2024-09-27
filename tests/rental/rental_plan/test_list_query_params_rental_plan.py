import json
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rental.rentalPlan.models import RentalPlan
from tests.rental.rental_plan.parent_case.rental_plan_api_test_case import (
    RentalPlanApiTestCase,
)

User = get_user_model()


class TestListQueryParamsRentalPlan(RentalPlanApiTestCase):
    def setUp(self):
        super().setUp()
        self.list_rental_plan: List[RentalPlan] = [
            self.create_rental_plan(
                amount=2222, name="cccc", periodicity=RentalPlan.BIWEEKLY
            ),
            self.create_rental_plan(
                amount=1111, name="bbbb", periodicity=RentalPlan.MONTHLY
            ),
            self.create_rental_plan(
                amount=3333,
                name=f"dddd{RentalPlan.MONTHLY}",
                periodicity=RentalPlan.WEEKLY,
            ),
            self.create_rental_plan(
                amount=4444, name="aaaa", periodicity=RentalPlan.WEEKLY
            ),
        ]

    def call_rental_plan_list(
        self,
        expected_index_ids: List[int],
        search_text: Optional[str] = None,
        order_by: Optional[str] = None,
        asc: Optional[bool] = None,
        print_json_response: bool = False,
    ) -> Dict[str, Any]:
        URL = reverse("rental-plan")
        if search_text or order_by or (asc is not None):
            query_params = []
            if search_text:
                query_params.append(f"searchText={search_text}")
            if order_by:
                query_params.append(f"orderBy={order_by}")
            if asc is not None:
                query_params.append(f"asc={asc}")
            for i, query_param in enumerate(query_params):
                URL += f"{('?' if i==0 else '&')}{query_param}"
        # print(URL)
        response = self.client.get(URL)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.validate_list_query_params_rental_plan(
            response_dict=response_dict, expected_index_ids=expected_index_ids
        )
        return response_dict

    def validate_list_query_params_rental_plan(
        self, response_dict, expected_index_ids: List[int]
    ):
        len_list = len(expected_index_ids)
        self.assertKey(
            response_dict=response_dict, key="count", expected=len_list
        )
        self.assertEqual(True, "results" in response_dict)
        results = response_dict["results"]
        self.assertIsInstance(results, list)
        self.assertEqual(len_list, len(results))
        for i, result in enumerate(results):
            self.assertIsInstance(result, dict)
            self.assertEqual(True, "id" in result)
            rental_plan_id = result["id"]
            rental_plan: RentalPlan = RentalPlan.objects.filter(
                id=rental_plan_id
            ).first()
            self.assertIsNotNone(rental_plan)
            if (
                rental_plan.id
                != self.list_rental_plan[expected_index_ids[i]].id
            ):
                print(
                    f"ids                {[v.id for v in self.list_rental_plan]}"
                )
                print(
                    f"expected_ids       {[self.list_rental_plan[indice].id for indice in expected_index_ids]}"
                )
                print(f"results ids        {[v['id'] for v in results]}")
                print(f"expected_index_ids {expected_index_ids}")
                print(
                    f"i={i} rental_plan.id={rental_plan.id} self.list_rental_plan[i].id={self.list_rental_plan[i].id}"
                )
                print([v["name"] for v in results])
            self.assertEqual(
                rental_plan.id, self.list_rental_plan[expected_index_ids[i]].id
            )

    def test_list_query_params_rental_plan(self):
        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()
        sorted_by_name = [3, 1, 0, 2]

        self.call_rental_plan_list(expected_index_ids=sorted_by_name)

        self.call_rental_plan_list(
            expected_index_ids=sorted_by_name[::-1], asc=False
        )

        sorted_by_amount = [1, 0, 2, 3]

        self.call_rental_plan_list(
            expected_index_ids=sorted_by_amount, order_by="amount"
        )

        self.call_rental_plan_list(
            expected_index_ids=sorted_by_amount[::-1],
            order_by="amount",
            asc=False,
        )

        sorted_by_pk = [0, 1, 2, 3]
        self.call_rental_plan_list(
            expected_index_ids=sorted_by_pk, order_by="pk"
        )

        self.call_rental_plan_list(
            expected_index_ids=sorted_by_pk[::-1], order_by="pk", asc=False
        )

        search = [1, 2]
        self.call_rental_plan_list(
            expected_index_ids=search,
            order_by="pk",
            search_text=RentalPlan.MONTHLY,
        )
