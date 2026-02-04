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
    )

    if attempts.filter(score__gte=assignment.pass_marks).exists():
        return redirect("assignments:student_assignment_list")

    if attempts.count() >= 2:
        return redirect("assignments:student_assignment_list")

    submission = Submission.objects.create(
        assignment=assignment,
        student=request.user,
        started_at=now(),
        attempt_number=attempts.count() + 1
    )

    return render(request, "assignments/student/exam_page.html", {
        "assignment": assignment,
        "questions": assignment.questions.all(),
        "submission": submission
    })

@group_required("Student")
def submit_exam(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = Submission.objects.get(assignment=assignment, student=request.user)

    total = 0
    for q in assignment.questions.all():
        selected = request.POST.get(str(q.id))
        if selected:
            correct = selected == q.correct_option
            if correct:
                total += q.marks

            Answer.objects.create(
                submission=submission,
                question=q,
                selected_option=selected,
                is_correct=correct
            )

    submission.score = total
    submission.status = "submitted"
    submission.submitted_at = now()
    submission.save()

    return redirect("assignments:exam_result", submission.id)

@group_required("Student")
def exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    passed = submission.score >= submission.assignment.pass_marks
    return render(request, "assignments/student/exam_result.html", {
        "submission": submission,
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
def trainer_assignment_create(request):
    if request.method == "POST":
        Assignment.objects.create(
            title=request.POST["title"],
            course_id=request.POST["course"],
            total_marks=request.POST["total_marks"],
            pass_marks=request.POST["pass_marks"],
            created_by=request.user
        )
        return redirect("assignments:trainer_assignment_list")

    return render(request, "assignments/trainer/trainer_assignment_create.html")

@group_required("Trainer")
def trainer_assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    return render(request, "assignments/trainer/trainer_assignment_submissions.html", {
        "assignment": assignment,
        "submissions": Submission.objects.filter(assignment=assignment)
    })

@group_required("Trainer")
def trainer_assignment_report(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    subs = Submission.objects.filter(assignment=assignment, status="submitted")

    return render(request, "assignments/trainer/trainer_assignment_report.html", {
        "assignment": assignment,
        "total": subs.count(),
        "avg_score": subs.aggregate(Avg("score"))["score__avg"] or 0,
        "toppers": subs.order_by("-score")[:5]
    })

# ================= ADMIN =================
@group_required("Admin")
def admin_pending_assignments(request):
    return render(request, "assignments/admin/admin_pending_assignments.html", {
        "assignments": Assignment.objects.filter(status="pending")
    })


@group_required("Admin")
def admin_approve_assignment(request, assignment_id):
    Assignment.objects.filter(id=assignment_id).update(status="approved")
    return redirect("assignments:admin_pending_assignments")



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
