from django.urls import path
from . import views
from .admin_users import *


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Dashboards
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    # Admin actions
    path("dashboard/admin/create-user/", views.admin_create_user, name="admin_create_user"),

    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/create/', views.admin_create_user, name='admin_create_user'),
    path('admin/users/created/', views.admin_user_created, name='admin_user_created'),
    path('admin/users/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),



]

