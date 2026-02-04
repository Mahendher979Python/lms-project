import math
from datetime import datetime
from django.http import JsonResponse
from core_settings.models import AdminSettings, TrainerSettings
from django.utils import timezone
from attendance.models import Attendance
from enrollments.models import Enrollment


#==============================================================================
# Admin Settings Business Logic
#==============================================================================
def _distance_in_meters(lat1, lon1, lat2, lon2):
    """
    Haversine formula to calculate distance in meters
    """
    R = 6371000  # Earth radius (meters)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def validate_attendance_rules(latitude, longitude):
    """
    Business rules for attendance:
    - Login time window
    - GPS radius check
    """

    settings = AdminSettings.get()

    # ⏰ LOGIN TIME WINDOW CHECK
    now = datetime.now().time()
    if settings.attendance_login_start and settings.attendance_login_end:
        if not (settings.attendance_login_start <= now <= settings.attendance_login_end):
            return JsonResponse(
                {"error": "Attendance login not allowed at this time"},
                status=403
            )

    # 📍 GPS RADIUS CHECK
    if settings.gps_required:
        if not latitude or not longitude:
            return JsonResponse(
                {"error": "GPS location required"},
                status=403
            )

        # 🔴 Replace with your office / institute coordinates
        OFFICE_LAT = 17.3850
        OFFICE_LNG = 78.4867

        distance = _distance_in_meters(
            OFFICE_LAT,
            OFFICE_LNG,
            float(latitude),
            float(longitude)
        )

        if distance > settings.gps_radius_meters:
            return JsonResponse(
                {"error": "You are outside allowed attendance location"},
                status=403
            )

    return None

#==============================================================================
# Trainer Settings Business Logic
#==============================================================================
def can_trainer_create_course(trainer):
    settings = TrainerSettings.get()
    return settings.can_create_courses


def can_trainer_edit_course(is_published):
    settings = TrainerSettings.get()
    if is_published and not settings.can_edit_published_course:
        return False
    return True


def can_trainer_delete_course():
    settings = TrainerSettings.get()
    return settings.can_delete_course


#==============================================================================
# Student Settings Business Logic
#==============================================================================

def is_student_approval_required():
    settings = AdminSettings.get()
    return settings.student_approval_required


def can_student_enroll(student):
    settings = AdminSettings.get()
    count = Enrollment.objects.filter(student=student).count()
    return count < settings.max_courses_per_student


def has_required_attendance(student, course=None):
    settings = AdminSettings.get()

    total = Attendance.objects.filter(
        user=student,
        status__in=["Approved", "Present"]
    ).count()

    present = Attendance.objects.filter(
        user=student,
        status="Present"
    ).count()

    if total == 0:
        return False

    percent = (present / total) * 100
    return percent >= settings.student_attendance_required_percent


def is_student_inactive(student):
    settings = AdminSettings.get()
    last_login = student.last_login

    if not last_login:
        return True

    days = (timezone.now() - last_login).days
    return days >= settings.auto_block_student_inactive_days
