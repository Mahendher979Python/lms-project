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
        student=request.user,
        status="submitted"
    ).select_related("assignment").order_by("-submitted_at")

    return render(
        request,
        "assignments/student/student_exam_history.html",
        {
            "submissions": submissions
        }
    )

@group_required("Student")
def download_certificate(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student=request.user
    )

    assignment = submission.assignment

    if submission.score < assignment.pass_marks:
        return HttpResponse("You are not eligible for certificate", status=403)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{assignment.title}_certificate.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(10.5 * cm, 26 * cm, "CERTIFICATE OF COMPLETION")

    # Body
    c.setFont("Helvetica", 14)
    c.drawCentredString(10.5 * cm, 22 * cm, "This is to certify that")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(10.5 * cm, 20.5 * cm, request.user.get_full_name() or request.user.username)

    c.setFont("Helvetica", 14)
    c.drawCentredString(
        10.5 * cm,
        18.5 * cm,
        f"has successfully completed the assignment"
    )

    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(10.5 * cm, 17 * cm, assignment.title)

    c.setFont("Helvetica", 12)
    c.drawCentredString(
        10.5 * cm,
        15 * cm,
        f"Score: {submission.score} / {assignment.total_marks}"
    )

    c.drawCentredString(
        10.5 * cm,
        13.5 * cm,
        f"Date: {submission.submitted_at.strftime('%d %B %Y')}"
    )

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
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.status = "rejected"
    assignment.save()

    return redirect("assignments:admin_pending_assignments")

@group_required("Admin")
def admin_overall_report(request):
    assignments = Assignment.objects.filter(status="approved")

    data = []
    for a in assignments:
        submissions = Submission.objects.filter(
            assignment=a,
            status="submitted"
        )
        data.append({
            "assignment": a,
            "total_students": submissions.count(),
            "average_score": submissions.aggregate(
                avg=Avg("score")
            )["avg"] or 0
        })

    return render(
        request,
        "assignments/admin/admin_overall_report.html",
        {
            "report_data": data
        }
    )

# ================= COMMON =================
def unauthorized(request):
    return render(request, "assignments/student/unauthorized.html")
