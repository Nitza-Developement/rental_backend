import json
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rental.tenant.models import Tenant
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)

User = get_user_model()


class TestListQueryParamsTenant(TenantApiTestCase):
    def setUp(self):
        self.list_tenant: List[Tenant] = [
            self.create_tenant(
                email="bbbb@gmail.com", name="cccc", isAdmin=True
            ),
            self.create_tenant(email="aaaabusca@gmail.com", name="bbbb"),
            self.create_tenant(email="cccc@gmail.com", name="ddddbusca"),
            self.create_tenant(email="dddd@gmail.com", name="aaaa"),
        ]
        self.create_tenant_user_admin(tenant=self.list_tenant[0])
        self.custom_user = self.create_user()

    def call_tenant_list(
        self,
        expected_index_ids: List[int],
        search_text: Optional[str] = None,
        order_by: Optional[str] = None,
        asc: Optional[bool] = None,
        print_json_response: bool = False,
    ) -> Dict[str, Any]:
        URL = reverse("tenant")
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
        self.validate_list_query_params_tenant(
            response_dict=response_dict, expected_index_ids=expected_index_ids
        )
        return response_dict

    def validate_list_query_params_tenant(
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
            tenant_id = result["id"]
            tenant: Tenant = Tenant.objects.filter(id=tenant_id).first()
            self.assertIsNotNone(tenant)
            if tenant.id != self.list_tenant[expected_index_ids[i]].id:
                print(f"ids                {[v.id for v in self.list_tenant]}")
                print(
                    f"expected_ids       {[self.list_tenant[indice].id for indice in expected_index_ids]}"
                )
                print(f"results ids        {[v['id'] for v in results]}")
                print(f"expected_index_ids {expected_index_ids}")
                print(
                    f"i={i} tenant.id={tenant.id} self.list_tenant[i].id={self.list_tenant[i].id}"
                )
                print([v["name"] for v in results])
            self.assertEqual(
                tenant.id, self.list_tenant[expected_index_ids[i]].id
            )

    def test_list_query_params_tenant(self):
        self.login(email=self.admin_email, password=self.admin_password)
        self.put_authentication_in_the_header()
        sorted_by_name = [3, 1, 0, 2]

        self.call_tenant_list(expected_index_ids=sorted_by_name)

        self.call_tenant_list(
            expected_index_ids=sorted_by_name[::-1], asc=False
        )

        sorted_by_email = [1, 0, 2, 3]

        self.call_tenant_list(
            expected_index_ids=sorted_by_email, order_by="email"
        )

        self.call_tenant_list(
            expected_index_ids=sorted_by_email[::-1],
            order_by="email",
            asc=False,
        )

        sorted_by_pk = [0, 1, 2, 3]
        self.call_tenant_list(expected_index_ids=sorted_by_pk, order_by="pk")

        self.call_tenant_list(
            expected_index_ids=sorted_by_pk[::-1], order_by="pk", asc=False
        )

        search_busca = [1, 2]
        self.call_tenant_list(
            expected_index_ids=search_busca, order_by="pk", search_text="busca"
        )
