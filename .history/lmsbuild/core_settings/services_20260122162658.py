import math
from datetime import datetime
from django.http import JsonResponse
from core_settings.models import AdminSettings


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
