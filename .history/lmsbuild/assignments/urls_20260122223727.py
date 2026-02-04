from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path("student/", views.student_assignment_list, name="student_assignment_list"),
    path("student/<int:assignment_id>/start/", views.start_exam, name="start_exam"),
    path("student/<int:assignment_id>/submit/", views.submit_exam, name="submit_exam"),
    path("student/result/<int:submission_id>/", views.exam_result, name="exam_result"),
]
