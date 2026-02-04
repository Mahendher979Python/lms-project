from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .models import Assignment, Question, Submission, Answer
from enrollments.models import Enrollment   # mee project lo unte

# Create your views here.

# View for students to see available assignments
#=========================================================
@login_required
def student_assignment_list(request):
    assignments = Assignment.objects.filter(status="approved")

    # Optional: enrollment filter
    assignments = assignments.filter(
        course__in=Enrollment.objects.filter(
            student=request.user
        ).values_list("course", flat=True)
    )

    return render(request, "assignments/student_assignment_list.html", {
        "assignments": assignments
    })

@login_required
def submit_exam(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = get_object_or_404(
        Submission, assignment=assignment, student=request.user
    )

    if submission.status != "started":
        return redirect("assignments:exam_result", submission_id=submission.id)

    total_score = 0

    for question in assignment.questions.all():
        selected = request.POST.get(str(question.id))
        if not selected:
            continue

        is_correct = selected == question.correct_option
        if is_correct:
            total_score += question.marks

        Answer.objects.create(
            submission=submission,
            question=question,
            selected_option=selected,
            is_correct=is_correct
        )

    submission.score = total_score
    submission.status = "submitted"
    submission.submitted_at = now()
    submission.save()

    return redirect("assignments:exam_result", submission_id=submission.id)


@login_required
def exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission, id=submission_id, student=request.user
    )

    assignment = submission.assignment
    passed = submission.score >= assignment.pass_marks

    return render(request, "assignments/result.html", {
        "submission": submission,
        "assignment": assignment,
        "passed": passed
    })


# View for trainers to create assignments
#=========================================================
@login_required
def trainer_assignment_list(request):
    assignments = Assignment.objects.filter(created_by=request.user)

    return render(request, "assignments/trainer_assignment_list.html", {
        "assignments": assignments
    })

@login_required
def trainer_assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, id=assignment_id, created_by=request.user
    )

    submissions = Submission.objects.filter(assignment=assignment)

    return render(request, "assignments/trainer_assignment_submissions.html", {
        "assignment": assignment,
        "submissions": submissions
    })

@login_required
def trainer_submission_review(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        assignment__created_by=request.user
    )

    answers = submission.answers.select_related("question")

    return render(request, "assignments/trainer_submission_review.html", {
        "submission": submission,
        "answers": answers
    })

#Pending Assignments List for Admin
#=========================================================
@login_required
def admin_pending_assignments(request):
    if not request.user.is_staff:
        return redirect("assignments:student_assignment_list")

    assignments = Assignment.objects.filter(status="pending")

    return render(request, "assignments/admin_pending_assignments.html", {
        "assignments": assignments
    })


#🔍 Assignment Review Page
#=========================================================
@login_required
def admin_assignment_review(request, assignment_id):
    if not request.user.is_staff:
        return redirect("assignments:student_assignment_list")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    questions = assignment.questions.all()

    return render(request, "assignments/admin_assignment_review.html", {
        "assignment": assignment,
        "questions": questions
    })

#✅ Approve Assignment
#=========================================================
@login_required
def admin_approve_assignment(request, assignment_id):
    if not request.user.is_staff:
        return redirect("assignments:student_assignment_list")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.status = "approved"
    assignment.save()

    return redirect("assignments:admin_pending_assignments")

#❌ Reject Assignment
#=========================================================
@login_required
def admin_reject_assignment(request, assignment_id):
    if not request.user.is_staff:
        return redirect("assignments:student_assignment_list")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.status = "rejected"
    assignment.save()

    return redirect("assignments:admin_pending_assignments")