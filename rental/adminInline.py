from django.contrib import admin
from rental.models import (
    TenantUser,
    Client,
    Vehicle,
    VehiclePlate,
    VehiclePicture,
    Note,
    StageUpdate,
    TollDue,
    TrackerHeartBeatData,
    Contract,
)


class TenantUserInline(admin.TabularInline):
    model = TenantUser
    extra = 0


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0


class VehiclePlateInline(admin.TabularInline):
    model = VehiclePlate
    extra = 0


class VehiclePictureInline(admin.TabularInline):
    model = VehiclePicture
    extra = 0


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class StageUpdateInline(admin.TabularInline):
    model = StageUpdate
    extra = 0


class TollDueInline(admin.TabularInline):
    model = TollDue
    extra = 0


class TrackerHeartbeatDataInline(admin.TabularInline):
    model = TrackerHeartBeatData
    extra = 0


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
