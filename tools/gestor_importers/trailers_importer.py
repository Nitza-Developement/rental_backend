from rental.tenant.models import Tenant
from rental.vehicle.models import Vehicle
from rental.vehicle.models import VehiclePlate


class TrailerImporter:
    sql_file = "trailers_importer.sql"

    def save(self, rows: list[tuple], tenant: Tenant | None = None):
        if tenant is None:
            tenant = Tenant.objects.first()
        if tenant is None:
            raise Exception("No tenant found")

        imported = 0
        for row in rows:
            vin = row[0]
            if len(vin) > 17:
                continue
            if Vehicle.objects.filter(vin=vin).exists():
                continue

            vehicle = Vehicle(
                vin=vin,
                year=row[1],
                type=row[3],
                status=Vehicle.AVAILABLE if row[4] == 1 else Vehicle.UNAVAILABLE,
                make=row[5],
                tenant=tenant,
            )
            vehicle.save()

            if (
                row[2]
                and row[2] != ""
                and not VehiclePlate.objects.filter(plate=row[2]).exists()
            ):
                plate = VehiclePlate(
                    vehicle=vehicle,
                    plate=row[2],
                )
                plate.save()
            else:
                plate = None

            print("============")
            print(">>> Vehicle", vehicle)
            print(">>> Plate", plate)
            print(row)
            print("############")
            imported += 1

        print(f"Imported vehicles: {imported}/{len(rows)}")
