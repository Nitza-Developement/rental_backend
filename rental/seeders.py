# django-seeding must be bug in order priority to run
# https://github.com/suliman-99/django-seeding/issues/3

from rental.seeders.tenant import TenantSeeder

from rental.seeders.tenant_user import TenantUserSeeder

from rental.seeders.rental_plan import RentalPlanSeeder

from rental.seeders.vehicle import VehicleSeeder

from rental.seeders.vehicle_plate import VehiclePlateSeeder

from rental.seeders.vehicle_picture import VehiclePictureSeeder

from rental.seeders.client import ClientSeeder

from rental.seeders.contract import ContractSeeder

from rental.seeders.inspections import InspectionSeeder
