from django.urls import path
from rental.user.api import LogoutView, update_profile, get_user_data
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rental.tenant.api import ListAndCreateTenantsView, GetUpdateAndDeleteATenantView
from rental.tenantUser.api import (
    ListAndCreateTenantUserView,
    GetUpdateAndDeleteTenantUserView,
)
from rental.client.api import ClientListAndCreateView, ClientGetUpdateAndDeleteView
from rental.vehicle.api import ListAndCreateVehicleView, GetUpdateAndDeleteVehicleView, get_vehicle_timeline
from rental.rentalPlan.api import (
    ListAndCreateRentalPlansView,
    GetUpdateAndDeleteARentalPlanView,
)
from rental.notes.api import ListAndCreateNotesView, GetUpdateAndDeleteANoteView
from rental.toll.api import ListAndCreateTollDuesView, GetUpdateAndDeleteATollDueView
from rental.contract.api import ListAndCreateContractView, GetUpdatePatchContractView, get_contract_timeline
from rental.tracker.api import (
    ListAndCreateTrackersView,
    ListAndCreateTrackerHeartBeatDataView,
    GetUpdateAndDeleteATrackerView,
    DeleteTrackerHeartBeatDataView,
)
from rental.forms.api import (
    FormListAndCreateView,
    FormImportView,
    FormCloneView,
    FormGetUpdateAndDeleteView,
    CardCreateUpdateAndDeleteView,
)

from rental.inspections.api import InspectionListAndCreateView, FormsAndVehiclesGet

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="refresh"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("user", get_user_data, name="user-data"),
    path("profile", update_profile, name="update-profile"),
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
        name="vehicle-actions",
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
        "forms/cards",
        CardCreateUpdateAndDeleteView.as_view(),
        name="add-card",
    ),
    path(
        "forms/cards/<int:card_id>",
        CardCreateUpdateAndDeleteView.as_view(),
        name="delete-card",
    ),
    path("forms/clone", FormCloneView.as_view(), name="clone-form"),
    path("inspections", InspectionListAndCreateView.as_view(), name="inspections"),
    path(
        "inspections/forms-and-vehicles",
        FormsAndVehiclesGet.as_view(),
        name="forms-and-vehicles",
    ),
]
