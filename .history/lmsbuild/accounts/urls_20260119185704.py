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

    # =========================
    # AUTH
    # =========================
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),


    # =========================
    # DASHBOARDS
    # =========================
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),


    # =========================
    # ADMIN – USER MANAGEMENT (ONLY ONE SET)
    # =========================
    path("admin/users/", admin_users, name="admin_users"),
    path("admin/users/create/", admin_create_user, name="admin_create_user"),
    path("admin/users/created/", admin_user_created, name="admin_user_created"),
    path("admin/users/edit/<int:user_id>/", admin_edit_user, name="admin_edit_user"),
    path("admin/users/delete/<int:user_id>/", admin_delete_user, name="admin_delete_user"),


    # =========================
    # ADMIN – TRAINERS
    # =========================
    path("admin/trainers/", views.admin_trainer_list, name="admin_trainer_list"),
    path("admin/trainers/create/", views.admin_trainer_create, name="admin_trainer_create"),
    path("admin/trainers/edit/<int:trainer_id>/", views.admin_trainer_edit, name="admin_trainer_edit"),


    # =========================
    # ADMIN – STUDENTS
    # =========================
    path("admin/students/", views.admin_student_list, name="admin_student_list"),
    path("admin/students/create/", views.admin_student_create, name="admin_student_create"),
    path("admin/students/edit/<int:student_id>/", views.admin_student_edit, name="admin_student_edit"),


    # =========================
    # ADMIN – STAFF
    # =========================
    path("admin/staff/", views.admin_staff_list, name="admin_staff_list"),
    path("admin/staff/create/", views.admin_staff_create, name="admin_staff_create"),
]
