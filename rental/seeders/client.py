from rental.models import Client, Tenant
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry


@SeederRegistry.register
class ClientSeeder(seeders.ModelSeeder):
    id = "ClientSeeder"
    priority = 7
    model = Client
    tenant = Tenant.objects.first()
    data = [
        {
            "email": "zxczx@gmail.com",
            "name": "Random guy 1",
            "phone_number": "+8 (737) 236-5655",
            "tenant": tenant,
        },
        {
            "email": "zxcza@gmail.com",
            "name": "Random guy 2",
            "phone_number": "+8 (737) 236-5656",
            "tenant": tenant,
        },
        {
            "email": "zxczb@gmail.com",
            "name": "Random guy 3",
            "phone_number": "+8 (737) 236-5657",
            "tenant": tenant,
        },
    ]
