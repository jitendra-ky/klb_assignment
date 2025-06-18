"""URL configuration for the users app."""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("", views.index, name="users_index"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/register/", views.RegisterView.as_view(), name="register"), # public endpoint
    path("api/profile/", views.ProfileView.as_view(), name="profile"), # protected endpoint

    path("api/telegram/register/", views.TelegramRegisterView.as_view(), name="telegram-register"),
]
