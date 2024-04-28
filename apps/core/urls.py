from django.urls import path
from apps.core.user.api import LogoutView, update_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.core.tenant.api import ListAndCreateTenantsView, GetUpdateAndDeleteATenantView
from apps.core.tenantUser.api import ListAndCreateTenantUserView, GetUpdateAndDeleteTenantUserView
from apps.core.client.api import ClientListAndCreateView, ClientGetUpdateAndDeleteView


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
    path('client/<int:client_id>', ClientGetUpdateAndDeleteView.as_view(), name='client-actions')
]
