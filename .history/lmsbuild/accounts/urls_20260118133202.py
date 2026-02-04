

from django.urls import path
from . import views
from .views import (
    login_view, logout_view, dashboard,
    admin_dashboard, trainer_dashboard, student_dashboard
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard, name="dashboard"),

    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("trainer-dashboard/", trainer_dashboard, name="trainer_dashboard"),
    path("student-dashboard/", student_dashboard, name="student_dashboard"),

      path("", views.home, name="home"),
]