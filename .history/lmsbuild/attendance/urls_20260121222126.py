from django.urls import path
from . import views

urlpatterns = [
    path("student/attendance/", views.student_attendance, name="student_attendance"),
    path("trainer/attendance/", views.trainer_attendance, name="trainer_attendance"),
    path("attendance-login/", views.attendance_login, name="attendance_login"),
    path("attendance-logout/", views.attendance_logout, name="attendance_logout"),


    path("student/attendance/", views.student_attendance, name="student_attendance"),
    path("trainer/attendance/", views.trainer_attendance, name="trainer_attendance"),
    path("attendance-login/", views.attendance_login, name="attendance_login"),
    path("attendance-logout/", views.attendance_logout, name="attendance_logout"),
]

