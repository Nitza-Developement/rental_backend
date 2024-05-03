from django.urls import path
from rental.user.api import LogoutView, update_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rental.tenant.api import ListAndCreateTenantsView, GetUpdateAndDeleteATenantView
from rental.tenantUser.api import ListAndCreateTenantUserView, GetUpdateAndDeleteTenantUserView
from rental.client.api import ClientListAndCreateView, ClientGetUpdateAndDeleteView
from rental.vehicle.api import ListAndCreateVehicleView, GetUpdateAndDeleteVehicleView
from rental.rentalPlan.api import ListAndCreateRentalPlansView, GetUpdateAndDeleteARentalPlanView
from rental.notes.api import ListAndCreateNotesView, GetUpdateAndDeleteANoteView
from rental.toll.api import ListAndCreateTollDuesView, GetUpdateAndDeleteATollDueView
from rental.contract.api import ListAndCreateContractView, GetUpdatePatchContractView
from rental.tracker.api import ListAndCreateTrackersView, ListAndCreateTrackerHeartBeatDataView, GetUpdateAndDeleteATrackerView, DeleteTrackerHeartBeatDataView


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name="login"),
    path('login/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('profile', update_profile, name="update-profile"),

    path('tenant', ListAndCreateTenantsView.as_view(), name="tenant"),
    path('tenant/<int:tenant_id>', GetUpdateAndDeleteATenantView.as_view(), name="tenant-actions"),

    path('tenantUser', ListAndCreateTenantUserView.as_view(), name="tenantUser"),
    path('tenantUser/<int:tenantUser_id>', GetUpdateAndDeleteTenantUserView.as_view(), name="tenantUser-actions"),

    path('client', ClientListAndCreateView.as_view(), name='client'),
    path('client/<int:client_id>', ClientGetUpdateAndDeleteView.as_view(), name='client-actions'),

    path('vehicle', ListAndCreateVehicleView.as_view(), name='vehicle'),
    path('vehicle/<str:search_by>', GetUpdateAndDeleteVehicleView.as_view(), name='vehicle-actions'),
    
    path('rental-plan', ListAndCreateRentalPlansView.as_view(), name='rental-plan'),
    path('rental-plan/<int:rental_plan_id>', GetUpdateAndDeleteARentalPlanView.as_view(), name='rental-plan-actions'),
    
    path('contract', ListAndCreateContractView.as_view(), name='contract'),
    path('contract/<int:contract_id>', GetUpdatePatchContractView.as_view(), name='contract-actons'),
    
    path('notes', ListAndCreateNotesView.as_view(), name='notes'),
    path('notes/<int:note_id>', GetUpdateAndDeleteANoteView.as_view(), name='notes-actions'),

    path('toll-due', ListAndCreateTollDuesView.as_view(), name='toll-due'),
    path('toll-due/<int:toll_due_id>', GetUpdateAndDeleteATollDueView.as_view(), name='toll-due-actions'),
    
    path('tracker', ListAndCreateTrackersView.as_view(), name='tracker'),
    path('tracker/<int:tracker_id>', GetUpdateAndDeleteATrackerView.as_view(), name='tracker-actions'),
    path('tracker-heartbeat', ListAndCreateTrackerHeartBeatDataView.as_view(), name='tracker-heartbeat'),
    path('tracker-heartbeat/<int:heartbeat_id>', DeleteTrackerHeartBeatDataView.as_view(), name='tracker-heartbeat-actions'),
]
