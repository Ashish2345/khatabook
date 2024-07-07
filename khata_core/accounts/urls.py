from django.urls import path

from .views import DashboardView, LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
