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



from functools import wraps
from django.http import JsonResponse
from core_settings.models import AdminSettings


def maintenance_guard(view_func):
    """
    Blocks all actions if site is under maintenance
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        settings = AdminSettings.get()
        if settings.maintenance_mode:
            return JsonResponse(
                {"error": "System under maintenance"},
                status=503
            )
        return view_func(request, *args, **kwargs)
    return _wrapped


def attendance_required(view_func):
    """
    Allows attendance only if admin enabled it
    """
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
