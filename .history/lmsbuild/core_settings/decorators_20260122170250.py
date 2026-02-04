from functools import wraps
from django.http import JsonResponse
from core_settings.models import AdminSettings, TrainerSettings

#  Admin Settings Decorators
def maintenance_guard(view_func):
    """
    Blocks all actions if system is in maintenance mode
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
    Allows attendance actions only if admin enabled attendance
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

#==============================================================================

# Trainer Settings Decorators
#==============================================================================
def trainer_attendance_required(view_func):
    """
    Blocks trainer attendance if disabled by admin
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.role == "trainer":
            settings = TrainerSettings.get()
            if not settings.attendance_mandatory:
                return JsonResponse(
                    {"error": "Trainer attendance disabled"},
                    status=403
                )
        return view_func(request, *args, **kwargs)
    return _wrapped
