from rental.client.models import Client
from rental.tenant.models import Tenant


class ClientsImporter:
    sql_file = "clients_importer.sql"

    def save(self, rows: list[tuple], tenant: Tenant | None = None):
        if tenant is None:
            tenant = Tenant.objects.first()
        if tenant is None:
            raise Exception("No tenant found")

        imported = 0
        for row in rows:
            (email, phone, name) = row
            if not phone or not email:
                continue
            if (
                Client.objects.filter(email=email).exists()
                or Client.objects.filter(phone_number=phone).exists()
            ):
                continue

            client = Client(
                email=email,
                phone_number=phone,
                name=name,
                tenant=tenant,
            )
            client.save()

            print("============")
            print(">>> Client", client)
            print(row)
            print("############")
            imported += 1

        print(f"Imported clients: {imported}/{len(rows)}")
