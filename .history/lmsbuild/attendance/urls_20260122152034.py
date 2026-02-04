from django.urls import path
from . import views

urlpatterns = [
    # STUDENT
    path("student/", views.student_attendance, name="student_attendance"),

    # TRAINER
    path("trainer/", views.trainer_attendance, name="trainer_attendance"),

    # LOGIN / LOGOUT
    path("login/", views.attendance_login, name="attendance_login"),
    path("logout/", views.attendance_logout, name="attendance_logout"),

    # ADMIN (RENAME)
    path("hr/", views.admin_attendance_list, name="admin_attendance_list"),
    path("hr/add/", views.admin_attendance_create, name="admin_attendance_create"),
    path("hr/edit/<int:pk>/", views.admin_attendance_edit, name="admin_attendance_edit"),
    path("hr/delete/<int:pk>/", views.admin_attendance_delete, name="admin_attendance_delete"),
]


