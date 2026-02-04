from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [

    # ================= STUDENT =================
    path("student/", views.student_assignment_list, name="student_assignment_list"),
    path("student/<int:assignment_id>/start/", views.start_exam, name="start_exam"),
    path("student/<int:assignment_id>/submit/", views.submit_exam, name="submit_exam"),
    path("student/result/<int:submission_id>/", views.exam_result, name="exam_result"),
    path("student/history/", views.student_exam_history, name="student_exam_history"),
    path("student/certificate/<int:submission_id>/", views.download_certificate, name="download_certificate"),

    # ================= TRAINER =================
    path("trainer/assignments/", views.trainer_assignment_list, name="trainer_assignment_list"),
    path("trainer/assignment/<int:assignment_id>/submissions/", views.trainer_assignment_submissions, name="trainer_assignment_submissions"),
    path("trainer/submission/<int:submission_id>/review/", views.trainer_submission_review, name="trainer_submission_review"),
    path("trainer/assignment/<int:assignment_id>/report/", views.trainer_assignment_report, name="trainer_assignment_report"),

    # ================= ADMIN =================
    path("admin/assignments/pending/", views.admin_pending_assignments, name="admin_pending_assignments"),
    path("admin/assignment/<int:assignment_id>/review/", views.admin_assignment_review, name="admin_assignment_review"),
    path("admin/assignment/<int:assignment_id>/approve/", views.admin_approve_assignment, name="admin_approve_assignment"),
    path("admin/assignment/<int:assignment_id>/reject/", views.admin_reject_assignment, name="admin_reject_assignment"),
    path("admin/reports/", views.admin_overall_report, name="admin_overall_report"),

    # ================= COMMON =================
    path("unauthorized/", views.unauthorized, name="unauthorized"),
]
