from functools import wraps
from django.http import JsonResponse
from core_settings.models import AdminSettings


def attendance_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        settings = AdminSettings.get()
        if not settings.attendance_enabled:
            return JsonResponse(
                {"error": "Attendance disabled by admin"},
                status=403
            )
        return view_func(request, *args, **kwargs)
    return _wrapped
