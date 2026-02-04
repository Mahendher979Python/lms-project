from django.urls import path
from . import views

urlpatterns = [
    path(
        "student/attendance/",
        views.student_attendance,
        name="student_attendance"
    ),
    path(
        "trainer/attendance/",
        views.trainer_attendance,
        name="trainer_attendance"
    ),
]
