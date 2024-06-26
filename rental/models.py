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
from rental.forms.models import (
    Form,
    Card,
    Field,
    CheckOption,
    FieldResponse,
)
from auditlog.registry import auditlog
from rental.inspections.models import Inspection

auditlog.register(User)
auditlog.register(TollDue)
auditlog.register(Tenant)
auditlog.register(Client)
auditlog.register(RentalPlan)
auditlog.register(TenantUser)
auditlog.register(StageUpdate)
auditlog.register(Contract)
auditlog.register(Note)
auditlog.register(Vehicle)
auditlog.register(VehiclePlate)
auditlog.register(Inspection)
