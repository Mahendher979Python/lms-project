from functools import wraps
from django.http import JsonResponse
from core_settings.models import AdminSettings, TrainerSettings

from django.shortcuts import redirect, render
from core_settings.services import (
    is_student_approval_required,
    is_student_inactive,
)

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




def student_approval_required(view_func):
    """
    Blocks student if admin approval required
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.role == "student":
            if is_student_approval_required() and not request.user.is_approved:
                return render(request, "403.html")
        return view_func(request, *args, **kwargs)
    return _wrapped


def student_active_required(view_func):
    """
    Blocks inactive students automatically
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.role == "student":
            if is_student_inactive(request.user):
                return render(request, "403.html")
        return view_func(request, *args, **kwargs)
    return _wrapped
