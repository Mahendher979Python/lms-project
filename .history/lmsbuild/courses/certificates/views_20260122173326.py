from core_settings.services import has_required_attendance


@login_required
def generate_certificate(request, course_id):
    if request.user.role != "student":
        return render(request, "403.html")

    if not has_required_attendance(request.user):
        return render(request, "certificates/not_eligible.html")

    # generate certificate
