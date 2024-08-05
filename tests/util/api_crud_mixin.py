import json
from typing import Any, Dict, Optional

from rest_framework import status


class ApiCrudMixin:
    def call_create(
        self,
        url: str,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        response = self.client.post(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_update(
        self,
        url: str,
        payload: Dict[str, Any],
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Optional[Dict[str, Any]]:
        response = self.client.put(url, payload)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return None
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return None
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return None
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return None
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict

    def call_retrieve(
        self,
        url: str,
        unauthorized: bool = False,
        forbidden: bool = False,
        bad_request: bool = False,
        not_found: bool = False,
        print_json_response: bool = False,
    ) -> Dict:
        response = self.client.get(url)
        if print_json_response:
            response_dict = json.loads(str(response.content, encoding="utf8"))
            pretty = json.dumps(response_dict, indent=4)
            print(pretty)
        if unauthorized:
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )
            return
        elif bad_request:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            return
        elif not_found:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            return
        elif forbidden:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            return
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = json.loads(str(response.content, encoding="utf8"))
        return response_dict
