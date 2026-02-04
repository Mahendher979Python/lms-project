from django.urls import path
from . import views

urlpatterns = [
    path("student/attendance/", views.student_attendance, name="student_attendance"),
    path("trainer/attendance/", views.trainer_attendance, name="trainer_attendance"),
    path("attendance-login/", views.attendance_login, name="attendance_login"),
    path("attendance-logout/", views.attendance_logout, name="attendance_logout"),

    path("admin/attendance/", views.admin_attendance_list, name="admin_attendance_list"),
    path("attendance/admin/", views.admin_attendance_list, name="admin_attendance_list")
    path("admin/attendance/add/", views.admin_attendance_create, name="admin_attendance_create"),
    path("admin/attendance/<int:pk>/edit/", views.admin_attendance_edit, name="admin_attendance_edit"),
    path("admin/attendance/<int:pk>/delete/", views.admin_attendance_delete, name="admin_attendance_delete"),
]

