from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.http import HttpResponse
from django.db.models import Avg

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from .models import Assignment, Question, Submission, Answer
from enrollments.models import Enrollment
from .decorators import group_required
from django.contrib.auth.decorators import login_required

#================= STUDENT =================

@group_required("Student")
def student_assignment_list(request):
    assignments = Assignment.objects.filter(
        status="approved",
        course__in=Enrollment.objects.filter(
            student=request.user
        ).values_list("course", flat=True)
    )
    return render(request, "assignments/student/student_assignment_list.html", {
        "assignments": assignments
    })

@group_required("Student")
def start_exam(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, status="approved")

    attempts = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).order_by("-attempt_number")

    if attempts.filter(score__gte=assignment.pass_marks).exists():
        return redirect("assignments:student_assignment_list")

    if attempts.count() >= 2:
        return redirect("assignments:student_assignment_list")

    attempt_no = attempts.first().attempt_number + 1 if attempts.exists() else 1

    submission = Submission.objects.create(
        assignment=assignment,
        student=request.user,
        status="started",
        started_at=now(),
        attempt_number=attempt_no
    )

    return render(request, "assignments/student/exam_page.html", {
        "assignment": assignment,
        "questions": assignment.questions.all(),
        "submission": submission
    })

@group_required("Student")
def submit_exam(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = get_object_or_404(Submission, assignment=assignment, student=request.user)

    if submission.status != "started":
        return redirect("assignments:exam_result", submission_id=submission.id)

    total_score = 0

    for q in assignment.questions.all():
        selected = request.POST.get(str(q.id))
        if selected:
            is_correct = selected == q.correct_option
            if is_correct:
                total_score += q.marks

            Answer.objects.create(
                submission=submission,
                question=q,
                selected_option=selected,
                is_correct=is_correct
            )

    submission.score = total_score
    submission.status = "submitted"
    submission.submitted_at = now()
    submission.save()

    return redirect("assignments:exam_result", submission_id=submission.id)

@group_required("Student")
def exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    assignment = submission.assignment
    passed = submission.score >= assignment.pass_marks

    return render(request, "assignments/student/result.html", {
        "submission": submission,
        "assignment": assignment,
        "passed": passed
    })

@group_required("Student")
def student_exam_history(request):
    submissions = Submission.objects.filter(
        student=request.user
    ).order_by("-submitted_at")

    return render(request, "assignments/student/student_exam_history.html", {
        "submissions": submissions
    })

@group_required("Student")
def download_certificate(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)

    if submission.score < submission.assignment.pass_marks:
        return HttpResponse("Not eligible")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=certificate.pdf"

    c = canvas.Canvas(response, pagesize=A4)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(10.5 * cm, 25 * cm, "CERTIFICATE OF COMPLETION")

    c.setFont("Helvetica", 14)
    c.drawCentredString(10.5 * cm, 21 * cm, f"{submission.student}")
    c.drawCentredString(10.5 * cm, 19 * cm, submission.assignment.title)
    c.drawCentredString(10.5 * cm, 17 * cm, f"Score: {submission.score}")

    c.showPage()
    c.save()
    return response

# ================= TRAINER =================
@group_required("Trainer")
def trainer_assignment_list(request):
    return render(request, "assignments/trainer/trainer_assignment_list.html", {
        "assignments": Assignment.objects.filter(created_by=request.user)
    })

@group_required("Trainer")
def trainer_assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    return render(request, "assignments/trainer/trainer_assignment_submissions.html", {
        "assignment": assignment,
        "submissions": Submission.objects.filter(assignment=assignment)
    })

@group_required("Trainer")
def trainer_submission_review(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        assignment__created_by=request.user
    )
    return render(request, "assignments/trainer/trainer_submission_review.html", {
        "submission": submission,
        "answers": submission.answers.select_related("question")
    })

@group_required("Trainer")
def trainer_assignment_report(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    subs = Submission.objects.filter(assignment=assignment, status="submitted")

    return render(request, "assignments/trainer/trainer_assignment_report.html", {
        "assignment": assignment,
        "total": subs.count(),
        "avg_score": subs.aggregate(avg=Avg("score"))["avg"] or 0,
        "toppers": subs.order_by("-score")[:5]
    })

# ================= ADMIN =================
@group_required("Admin")
def admin_pending_assignments(request):
    return render(request, "assignments/admin/admin_pending_assignments.html", {
        "assignments": Assignment.objects.filter(status="pending")
    })

@group_required("Admin")
def admin_assignment_review(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, "assignments/admin/admin_assignment_review.html", {
        "assignment": assignment,
        "questions": assignment.questions.all()
    })

@group_required("Admin")
def admin_approve_assignment(request, assignment_id):
    Assignment.objects.filter(id=assignment_id).update(status="approved")
    return redirect("assignments:admin_pending_assignments")

@group_required("Admin")
def admin_reject_assignment(request, assignment_id):
    Assignment.objects.filter(id=assignment_id).update(status="rejected")
    return redirect("assignments:admin_pending_assignments")

@group_required("Admin")
def admin_overall_report(request):
    return render(request, "assignments/admin/admin_overall_report.html", {
        "assignments": Assignment.objects.filter(status="approved")
    })

# ================= COMMON =================
def unauthorized(request):
    return render(request, "assignments/student/unauthorized.html")
