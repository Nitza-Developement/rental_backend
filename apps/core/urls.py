from django.urls import path
from apps.core.user.api import LogoutView, update_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name="login"),
    path('login/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('profile', update_profile, name="update-profile"),
]