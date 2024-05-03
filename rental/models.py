from rental.user.models import User
from rental.notes.models import Note
from rental.toll.models import TollDue
from rental.tenant.models import Tenant
from rental.client.models import Client
from rental.rentalPlan.models import RentalPlan
from rental.tenantUser.models import TenantUser
from rental.contract.models import StageUpdate, Contract
from rental.tracker.models import Tracker, TrackerHeartBeatData
from rental.vehicle.models import Vehicle, VehiclePlate, VehiclePicture
from auditlog.registry import auditlog


auditlog.register(User)
auditlog.register(TollDue)
auditlog.register(Tenant)
auditlog.register(Client)
auditlog.register(RentalPlan)
auditlog.register(TenantUser)
auditlog.register(StageUpdate)
auditlog.register(Contract)
auditlog.register(Vehicle)
auditlog.register(VehiclePlate)