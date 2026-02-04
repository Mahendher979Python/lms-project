from django.urls import path
from . import views
from . import admin_views

urlpatterns = [

    # ==================================================
    # STUDENT ATTENDANCE
    # ==================================================
    path(
        "student/",
        views.student_attendance,
        name="student_attendance"
    ),
    path(
        "student/login/",
        views.attendance_login,
        name="attendance_login"
    ),
    path(
        "student/logout/",
        views.attendance_logout,
        name="attendance_logout"
    ),

    # ==================================================
    # TRAINER ATTENDANCE
    # ==================================================
    path(
        "trainer/",
        views.trainer_attendance,
        name="trainer_attendance"
    ),

    # ==================================================
    # ADMIN ATTENDANCE – LIST & CRUD
    # ==================================================
    path(
        "admin/",
        admin_views.admin_attendance_list,
        name="admin_attendance_list"
    ),
    path(
        "admin/create/",
        admin_views.admin_attendance_create,
        name="admin_attendance_create"
    ),
    path(
        "admin/edit/<int:pk>/",
        admin_views.admin_attendance_edit,
        name="admin_attendance_edit"
    ),
    path(
        "admin/delete/<int:pk>/",
        admin_views.admin_attendance_delete,
        name="admin_attendance_delete"
    ),

    # ==================================================
    # ADMIN – APPROVAL SYSTEM
    # ==================================================
    path(
        "admin/approve/<int:pk>/",
        admin_views.admin_attendance_approve,
        name="admin_attendance_approve"
    ),
    path(
        "admin/reject/<int:pk>/",
        admin_views.admin_attendance_reject,
        name="admin_attendance_reject"
    ),

    # ==================================================
    # ADMIN – REPORTS & EXPORT
    # ==================================================
    path(
        "admin/reports/",
        admin_views.admin_monthly_report,
        name="admin_monthly_report"
    ),
    path(
        "admin/export/",
        admin_views.admin_attendance_export,
        name="admin_attendance_export"
    ),
]
