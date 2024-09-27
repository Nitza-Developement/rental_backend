import json
from typing import Dict, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.rental.rental_plan.parent_case.rental_plan_api_test_case import (
    RentalPlanApiTestCase,
)

User = get_user_model()


class TestListPaginationRentalPlan(RentalPlanApiTestCase):
    def setUp(self):
        super().setUp()
        user = self.custom_tenant_user_staff.default_tenant_user.user
        self.list_rental_plan = [
            self.create_rental_plan(user=user) for _ in range(20)
        ]
        self.total_count = len(self.list_rental_plan)
        self.maxDiff = None

    def call_list_rental_plan(
        self,
        len_list: int,
        expected_next: bool,
        expected_previous: bool,
        print_json_response: bool = False,
        page_size: Optional[int] = None,
        page: int = 0,
    ) -> Dict:
        URL = reverse("rental-plan")
        if page_size:
            URL = f"{URL}?pageSize={page_size}"
        if page > 0:
            URL = f"{URL}{'&'if page_size else '?'}page={page}"
        response = self.client.get(URL)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        self.validate_data_in_list_pagination(
            response_dict=response_dict,
            total_count=self.total_count,
            len_list=len_list,
            expected_next=expected_next,
            expected_previous=expected_previous,
            schema_validator=self.validate_rental_plan_in_list,
        )
        return response_dict

    def call_multiples_list(self):
        self.call_list_rental_plan(
            len_list=15,
            expected_next=True,
            expected_previous=False,
        )
        self.call_list_rental_plan(
            len_list=15, expected_next=True, expected_previous=False, page=1
        )
        self.call_list_rental_plan(
            len_list=5,
            expected_next=True,
            expected_previous=True,
            page=2,
            page_size=5,
        )

    def test_list_pagination_rental_plan(self):
        self.login(custom_user=self.custom_staff)
        self.put_authentication_in_the_header()
        self.call_multiples_list()
