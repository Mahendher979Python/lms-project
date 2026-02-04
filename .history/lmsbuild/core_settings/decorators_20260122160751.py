# core_settings/decorators.py

from functools import wraps
from django.http import JsonResponse
from core_settings.models import AdminSettings


def attendance_required(view_func):
    """
    This decorator checks:
    - Is attendance system enabled by admin?
    - If disabled, block the request globally
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        settings = AdminSettings.get()

        # 🔒 Global attendance switch
        if not settings.attendance_enabled:
            return JsonResponse(
                {"error": "Attendance is disabled by admin"},
                status=403
            )

        # ✅ Attendance enabled → continue original view
        return view_func(request, *args, **kwargs)

    return _wrapped_view
