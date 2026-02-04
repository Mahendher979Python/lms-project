from django.urls import path
from . import views
from .admin_users import (
    admin_users,
    admin_create_user,
    admin_user_created,
    admin_edit_user,
    admin_delete_user,
)

urlpatterns = [
    # Auth
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Dashboards
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    # Admin User Management (🔥 FIXED)
    path("admin/users/", admin_users, name="admin_users"),
    path("admin/users/create/", admin_create_user, name="admin_create_user"),
    path("admin/users/created/", admin_user_created, name="admin_user_created"),
    path("admin/users/edit/<int:user_id>/", admin_edit_user, name="admin_edit_user"),
    path("admin/users/delete/<int:user_id>/", admin_delete_user, name="admin_delete_user"),
]
