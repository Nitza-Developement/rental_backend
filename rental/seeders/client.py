from rental.models import Client
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry


@SeederRegistry.register
class ClientSeeder(seeders.ModelSeeder):
    id = "ClientSeeder"
    priority = 3
    model = Client
    tenant = 2
    data = [
        {
            "id": 1,
            "email": "zxczx@gmail.com",
            "name": "Random guy 1",
            "phone_number": "+8 (737) 236-5655",
            "tenant_id": tenant,
        },
        {
            "id": 2,
            "email": "zxcza@gmail.com",
            "name": "Random guy 2",
            "phone_number": "+8 (737) 236-5656",
            "tenant_id": tenant,
        },
        {
            "id": 3,
            "email": "zxczb@gmail.com",
            "name": "Random guy 3",
            "phone_number": "+8 (737) 236-5657",
            "tenant_id": tenant,
        },
    ]
