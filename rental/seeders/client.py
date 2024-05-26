from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from rental.models import Tenant, Client


@SeederRegistry.register
class ClientSeeder(seeders.ModelSeeder):
    id = "ClientSeeder"
    priority = 1
    model = Client
    tenant = Tenant.objects.get(id=2)
    data = [
        {
            "id": 1,
            "email": "zxczx@gmail.com",
            "name": "Random guy 1",
            "phone_number": "+8 (737) 236-5655",
            "tenant": tenant,
        },
        {
            "id": 2,
            "email": "zxcza@gmail.com",
            "name": "Random guy 2",
            "phone_number": "+8 (737) 236-5656",
            "tenant": tenant,
        },
        {
            "id": 3,
            "email": "zxczb@gmail.com",
            "name": "Random guy 3",
            "phone_number": "+8 (737) 236-5657",
            "tenant": tenant,
        },
    ]
