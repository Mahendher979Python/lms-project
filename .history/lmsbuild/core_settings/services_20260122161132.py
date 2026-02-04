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

from datetime import datetime
from django.http import JsonResponse
from core_settings.models import AdminSettings
import math


def is_within_radius(lat1, lon1, lat2, lon2, radius_m):
    """
    Haversine formula – distance in meters
    """
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return (2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))) <= radius_m


def validate_attendance_rules(lat, lng):
    """
    Checks:
    - Login time window
    - GPS radius
    """
    settings = AdminSettings.get()

    # ⏰ Time Window
    now = datetime.now().time()
    if settings.attendance_login_start and settings.attendance_login_end:
        if not (settings.attendance_login_start <= now <= settings.attendance_login_end):
            return JsonResponse(
                {"error": "Login not allowed at this time"},
                status=403
            )

    # 📍 GPS check
    if settings.gps_required:
        office_lat, office_lng = 17.3850, 78.4867  # 🔴 replace with your office coords
        if not is_within_radius(
            office_lat, office_lng,
            float(lat), float(lng),
            settings.gps_radius_meters
        ):
            return JsonResponse(
                {"error": "You are outside allowed location"},
                status=403
            )

    return None
