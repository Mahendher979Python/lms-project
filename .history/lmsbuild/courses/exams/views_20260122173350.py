from core_settings.services import has_required_attendance
from django.contrib import messages


@login_required
def start_exam(request, course_id):
    if not has_required_attendance(request.user):
        messages.error(request, "Attendance requirement not met")
        return redirect("student_dashboard")

    # allow exam
