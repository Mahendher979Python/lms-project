from core_settings.models import AdminSettings
from django.http import JsonResponse


def check_attendance_enabled():
    settings = AdminSettings.get()
    if not settings.attendance_enabled:
        return JsonResponse(
            {"error": "Attendance disabled by admin"},
            status=403
        )
    return None
