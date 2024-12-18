from django.contrib import admin
from django.contrib.auth.models import Group

from rental.adminInline import ClientInline
from rental.adminInline import ContractInline
from rental.adminInline import NoteInline
from rental.adminInline import StageUpdateInline
from rental.adminInline import TenantUserInline
from rental.adminInline import TollDueInline
from rental.adminInline import TrackerHeartbeatDataInline
from rental.adminInline import VehicleInline
from rental.adminInline import VehiclePictureInline
from rental.adminInline import VehiclePlateInline
from rental.contract_form.models import ContractForm
from rental.contract_form.models import ContractFormField
from rental.contract_form.models import ContractFormFieldResponse
from rental.contract_form.models import ContractFormTemplate
from rental.forms.models import Card
from rental.forms.models import Field
from rental.forms.models import FieldResponse
from rental.forms.models import Form
from rental.inspections.models import Inspection
from rental.models import Client
from rental.models import Contract
from rental.models import Note
from rental.models import RentalPlan
from rental.models import StageUpdate
from rental.models import Tenant
from rental.models import TenantUser
from rental.models import TollDue
from rental.models import Tracker
from rental.models import TrackerHeartBeatData
from rental.models import User
from rental.models import Vehicle
from rental.models import VehiclePicture
from rental.models import VehiclePlate
from rental.reminders.models import Reminder

admin.site.site_title = "Fleet Admin Site"
admin.site.site_header = "Administration Panel"
admin.site.index_title = "Dashboard"
admin.site.unregister(Group)

admin.site.register(Reminder)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "is_superuser", "date_joined"]
    search_fields = ("name", "email")
    date_hierarchy = "date_joined"


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "user", "tenant")
    search_fields = ("id", "user__name", "tenant__name")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone_number", "tenant")


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "isAdmin")
    search_fields = ("name", "email")
    date_hierarchy = "date_joined"
    inlines = [TenantUserInline, ClientInline, VehicleInline, ContractInline]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "active_plate",
        "type",
        "year",
        "make",
        "model",
        "trim",
        "vin",
        "nickname",
        "spare_tires",
        "status",
    )
    search_fields = ("id", "nickname", "model", "vin", "status")
    inlines = [VehiclePlateInline, VehiclePictureInline]


@admin.register(VehiclePicture)
class VehiclePictureAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "vehicle", "pinned")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "client",
        "vehicle",
        "rental_plan",
        "creation_date",
        "active_date",
        "end_date",
    )
    inlines = [StageUpdateInline, NoteInline, TollDueInline]


@admin.register(StageUpdate)
class StageUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "stage", "reason", "date")
    date_hierarchy = "date"


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body", "remainder", "contract", "user")
    search_fields = ("id", "subject", "contract__id")


@admin.register(TollDue)
class TollDueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "plate",
        "contract",
        "stage",
        "invoice",
        "invoiceNumber",
        "createDate",
        "note",
    )
    list_filter = ("stage",)
    search_fields = (
        "plate__plate",
        "contract__tenant__name",
        "contract__client__name",
        "invoice",
        "invoiceNumber",
    )
    date_hierarchy = "createDate"
    readonly_fields = ("createDate",)
    ordering = ("-createDate",)


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "vehicle", "created_date")
    list_filter = ("vehicle",)
    search_fields = ("name", "vehicle__make", "vehicle__model")
    date_hierarchy = "created_date"
    inlines = [TrackerHeartbeatDataInline]


@admin.register(TrackerHeartBeatData)
class TrackerHeartBeatDataAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "latitude", "longitude", "tracker")
    list_filter = ("tracker",)
    search_fields = ("timestamp", "latitude", "longitude", "tracker__name")
    date_hierarchy = "timestamp"


@admin.register(RentalPlan)
class RentalPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "amount", "periodicity")


@admin.register(VehiclePlate)
class VehiclePlateAdmin(admin.ModelAdmin):
    list_display = ("id", "plate", "is_active")


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "is_active")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")


@admin.register(FieldResponse)
class FieldResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "inspection", "created_at")


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("id", "form", "created_at")


@admin.register(ContractFormTemplate)
class ContractFormTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


@admin.register(ContractForm)
class ContractFormAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


@admin.register(ContractFormField)
class ContractFormFieldAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "type")


@admin.register(ContractFormFieldResponse)
class ContractFormFieldResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "form", "field")
