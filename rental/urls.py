from django.urls import include
from django.urls import path
from rest_framework import routers

from rental.client.api import ClientGetUpdateAndDeleteView
from rental.client.api import ClientListAndCreateView
from rental.contract.api import get_contract_timeline
from rental.contract.api import GetUpdatePatchContractView
from rental.contract.api import ListAndCreateContractView
from rental.contract_form.api import ContractFormFieldResponseCreateView
from rental.contract_form.api import ContractFormGetView
from rental.contract_form.api import ContractFormListAndCreateView
from rental.contract_form.api import ContractFormTemplateCloneView
from rental.contract_form.api import ContractFormTemplateGetUpdateAndDeleteView
from rental.contract_form.api import ContractFormTemplateListAndCreateView
from rental.forms.api import CardCreateUpdateAndDeleteView
from rental.forms.api import FormCloneView
from rental.forms.api import FormGetUpdateAndDeleteView
from rental.forms.api import FormImportView
from rental.forms.api import FormListAndCreateView
from rental.inspections.api import FormsAndVehiclesGet
from rental.inspections.api import InspectionCreateResponseView
from rental.inspections.api import InspectionGetUpdateAndDeleteView
from rental.inspections.api import InspectionListAndCreateView
from rental.notes.api import GetUpdateAndDeleteANoteView
from rental.notes.api import ListAndCreateNotesView
from rental.reminders.api import ReminderViewSet
from rental.rentalPlan.api import GetUpdateAndDeleteARentalPlanView
from rental.rentalPlan.api import ListAndCreateRentalPlansView
from rental.tenant.api import GetUpdateAndDeleteATenantView
from rental.tenant.api import ListAndCreateTenantsView
from rental.tenantUser.api import GetUpdateAndDeleteTenantUserView
from rental.tenantUser.api import ListAndCreateTenantUserView
from rental.toll.api import GetUpdateAndDeleteATollDueView
from rental.toll.api import ListAndCreateTollDuesView
from rental.tracker.api import DeleteTrackerHeartBeatDataView
from rental.tracker.api import GetUpdateAndDeleteATrackerView
from rental.tracker.api import ListAndCreateTrackerHeartBeatDataView
from rental.tracker.api import ListAndCreateTrackersView
from rental.user.api import CustomTokenObtainPairView
from rental.user.api import CustomTokenRefreshView
from rental.user.api import get_user_data
from rental.user.api import LogoutView
from rental.user.api import profile_change_password
from rental.user.api import update_profile
from rental.user.api import UserView
from rental.vehicle.api import get_vehicle_timeline
from rental.vehicle.api import GetUpdateAndDeleteVehicleView
from rental.vehicle.api import ListAndCreateVehicleView
from rental.vehicle.api import VehiclePlateView

router = routers.SimpleRouter()
router.register(r"users", UserView, basename="users")
router.register(r"reminders", ReminderViewSet, basename="reminders")

urlpatterns = [
    path("", include(router.urls)),
    path("login", CustomTokenObtainPairView.as_view(), name="login"),
    path("login/refresh", CustomTokenRefreshView.as_view(), name="refresh"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("user", get_user_data, name="user-data"),
    path("profile", update_profile, name="update-profile"),
    path("password", profile_change_password, name="change-password"),
    path("tenant", ListAndCreateTenantsView.as_view(), name="tenant"),
    path(
        "tenant/<int:tenant_id>",
        GetUpdateAndDeleteATenantView.as_view(),
        name="tenant-actions",
    ),
    path("tenantUser", ListAndCreateTenantUserView.as_view(), name="tenantUser"),
    path(
        "tenantUser/<int:tenantUser_id>",
        GetUpdateAndDeleteTenantUserView.as_view(),
        name="tenantUser-actions",
    ),
    path("client", ClientListAndCreateView.as_view(), name="client"),
    path(
        "client/<int:client_id>",
        ClientGetUpdateAndDeleteView.as_view(),
        name="client-actions",
    ),
    path("vehicle", ListAndCreateVehicleView.as_view(), name="vehicle"),
    path(
        "vehicle/<int:vehicle_id>",
        GetUpdateAndDeleteVehicleView.as_view(),
        name="vehicle-actions",
    ),
    path(
        "vehicle/<int:vehicle_id>/history",
        get_vehicle_timeline,
        name="vehicle-actions-history",
    ),
    path(
        "plates",
        VehiclePlateView.as_view(),
        name="vehicle-plates",
    ),
    path("rental-plan", ListAndCreateRentalPlansView.as_view(), name="rental-plan"),
    path(
        "rental-plan/<int:rental_plan_id>",
        GetUpdateAndDeleteARentalPlanView.as_view(),
        name="rental-plan-actions",
    ),
    path("contract", ListAndCreateContractView.as_view(), name="contract"),
    path(
        "contract/<int:contract_id>",
        GetUpdatePatchContractView.as_view(),
        name="contract-actions",
    ),
    path(
        "contract/<int:contract_id>/history",
        get_contract_timeline,
        name="contract-actions",
    ),
    path("notes", ListAndCreateNotesView.as_view(), name="notes"),
    path(
        "notes/<int:note_id>",
        GetUpdateAndDeleteANoteView.as_view(),
        name="notes-actions",
    ),
    path("toll-due", ListAndCreateTollDuesView.as_view(), name="toll-due"),
    path(
        "toll-due/<int:toll_due_id>",
        GetUpdateAndDeleteATollDueView.as_view(),
        name="toll-due-actions",
    ),
    path("tracker", ListAndCreateTrackersView.as_view(), name="tracker"),
    path(
        "tracker/<int:tracker_id>",
        GetUpdateAndDeleteATrackerView.as_view(),
        name="tracker-actions",
    ),
    path(
        "tracker-heartbeat",
        ListAndCreateTrackerHeartBeatDataView.as_view(),
        name="tracker-heartbeat",
    ),
    path(
        "tracker-heartbeat/<int:heartbeat_id>",
        DeleteTrackerHeartBeatDataView.as_view(),
        name="tracker-heartbeat-actions",
    ),
    path("forms", FormListAndCreateView.as_view(), name="forms"),
    path(
        "forms/<int:form_id>", FormGetUpdateAndDeleteView.as_view(), name="form-actions"
    ),
    path("forms/import", FormImportView.as_view(), name="import-forms"),
    path(
        "forms/<int:form_id>/cards",
        CardCreateUpdateAndDeleteView.as_view(),
        name="add-card",
    ),
    path(
        "forms/<int:form_id>/cards/<int:card_id>",
        CardCreateUpdateAndDeleteView.as_view(),
        name="card-actions",
    ),
    path("forms/clone", FormCloneView.as_view(), name="clone-form"),
    path("inspections", InspectionListAndCreateView.as_view(), name="inspections"),
    path(
        "inspections/forms-and-vehicles",
        FormsAndVehiclesGet.as_view(),
        name="forms-and-vehicles",
    ),
    path(
        "inspections/<int:inspection_id>",
        InspectionGetUpdateAndDeleteView.as_view(),
        name="inspections-actions",
    ),
    path(
        "inspections/response",
        InspectionCreateResponseView.as_view(),
        name="create-inspection-response",
    ),
    path(
        "contract-forms-template",
        ContractFormTemplateListAndCreateView.as_view(),
        name="contract-forms-template",
    ),
    path(
        "contract-forms-template/<int:pk>",
        ContractFormTemplateGetUpdateAndDeleteView.as_view(),
        name="contract-forms-template-action",
    ),
    path(
        "contract-forms-template/clone",
        ContractFormTemplateCloneView.as_view(),
        name="contract-forms-template-clone",
    ),
    path(
        "contract-forms",
        ContractFormListAndCreateView.as_view(),
        name="contract-forms",
    ),
    path(
        "contract-forms/<int:pk>",
        ContractFormGetView.as_view(),
        name="contract-form-action",
    ),
    path(
        "contract-forms/response",
        ContractFormFieldResponseCreateView.as_view(),
        name="contract-form-response",
    ),
]
