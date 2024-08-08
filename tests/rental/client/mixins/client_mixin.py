from typing import Dict, Optional

from django.contrib.auth import get_user_model
from faker import Faker

from rental.client.models import Client

fake = Faker()

User = get_user_model()


class ClientMixin:
    def create_client(self, user: User) -> Client:
        return Client.objects.create(
            name=fake.first_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            tenant=user.defaultTenantUser().tenant,
        )

    def validate_client_in_list(
        self,
        data: Dict,
        client_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
    ):
        if not client_id:
            self.assertEqual(True, "id" in data)
            client_id = data["id"]
        if not tenant_id:
            self.assertEqual(True, "tenant" in data)
            tenant_id = data["tenant"]
        client: Client = Client.objects.filter(id=client_id).first()
        self.assertIsNotNone(client)
        self.assertDictEqual(
            data,
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone_number": client.phone_number,
                "tenant": tenant_id,
            },
        )
