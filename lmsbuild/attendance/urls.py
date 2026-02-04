from django.urls import path
from . import views

urlpatterns = [

    # ================= STUDENT =================
    path("student/", views.student_attendance, name="student_attendance"),
    path("student/report/", views.student_attendance_report, name="student_attendance_report"),
    path("student/login/", views.attendance_login, name="attendance_login"),
    path("student/logout/", views.attendance_logout, name="attendance_logout"),


    # ================= TRAINER =================
    path("trainer/", views.trainer_attendance, name="trainer_attendance"),
    path("trainer/report/", views.trainer_attendance_report, name="trainer_attendance_report"),

    # ================= ADMIN =================
    path("admin/", views.admin_attendance_list, name="admin_attendance_list"),
    path("admin/create/", views.admin_attendance_create, name="admin_attendance_create"),
    path("admin/edit/<int:pk>/", views.admin_attendance_edit, name="admin_attendance_edit"),
    path("admin/delete/<int:pk>/", views.admin_attendance_delete, name="admin_attendance_delete"),

    # ===== ADMIN REPORTS =====
    path("admin/report/", views.admin_monthly_report, name="admin_monthly_report"),
    path("admin/export/", views.admin_attendance_export, name="admin_attendance_export"),
]
