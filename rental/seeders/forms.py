from rental.forms.models import Form
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry


@SeederRegistry.register
class FormSeeder(seeders.ModelSeeder):
    id = "FormSeeder"
    priority = 3
    model = Form
    tenant = 2
    data = [
        {
            "name": "Formulario",
            "is_active": True,
            "tenant_id": tenant,
        },
        {
            "name": "Formulario",
            "is_active": True,
            "tenant_id": tenant,
        },
    ]
