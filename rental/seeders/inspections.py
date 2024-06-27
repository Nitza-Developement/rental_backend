from rental.forms.models import Form, Field, Card, CheckOption, FieldResponse
from rental.inspections.models import Inspection
from rental.models import Tenant, TenantUser, Vehicle
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry


@SeederRegistry.register
class InspectionSeeder(seeders.Seeder):
    id = "InspectionSeeder"
    priority = 3

    def seed(self):
        tenants = Tenant.objects.all()
        tenants_user = TenantUser.objects.first()
        vehicle = Vehicle.objects.first()

        for tenant in tenants:

            form = Form.objects.create(name="Formulario", tenant=tenant)

            card = Card.objects.create(name="Card", form=form)

            field_text = Field.objects.create(name="Name", type=Field.TEXT, card=card)
            field_date = Field.objects.create(name="Date", type=Field.DATE, card=card)
            field_time = Field.objects.create(name="Time", type=Field.TIME, card=card)

            field_number = Field.objects.create(
                name="Age", type=Field.NUMBER, card=card
            )
            field_email = Field.objects.create(
                name="Email", type=Field.EMAIL, card=card
            )
            field_phone = Field.objects.create(
                name="Phone", type=Field.PHONE, card=card
            )

            field_check_option = Field.objects.create(
                name="Single check", type=Field.SINGLE_CHECK, card=card
            )

            option_pass = CheckOption.objects.create(
                name="Option pass",
                type=CheckOption.POINT_PASS,
                field=field_check_option,
            )
            CheckOption.objects.create(
                name="Option fail",
                type=CheckOption.POINT_FAIL,
                field=field_check_option,
            )

            inspection = Inspection.objects.create(
                form=form,
                tenant=tenant,
                vehicle=vehicle,
                tenantUser=tenants_user,
            )
            FieldResponse.objects.create(
                field=field_check_option,
                inspection=inspection,
                tenantUser=tenants_user,
                check_option_selected=option_pass,
                note="Esto es una nota opcional.",
            )

            FieldResponse.objects.create(
                field=field_text,
                inspection=inspection,
                tenantUser=tenants_user,
                content="Raul",
            )

            FieldResponse.objects.create(
                field=field_number,
                inspection=inspection,
                tenantUser=tenants_user,
                content="26",
            )

            FieldResponse.objects.create(
                field=field_date,
                inspection=inspection,
                tenantUser=tenants_user,
                content="Wed Jun 12 2024 20:00:00 GMT-0400 (Cuba Daylight Time)",
            )

            FieldResponse.objects.create(
                field=field_time,
                inspection=inspection,
                tenantUser=tenants_user,
                content="00:00",
            )

            FieldResponse.objects.create(
                field=field_email,
                inspection=inspection,
                tenantUser=tenants_user,
                content="email@example.com",
            )

            FieldResponse.objects.create(
                field=field_phone,
                inspection=inspection,
                tenantUser=tenants_user,
                content="56938300",
            )
