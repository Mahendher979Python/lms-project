from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.timezone import now
from .models import Attendance


@receiver(user_logged_in)
def mark_login_attendance(sender, request, user, **kwargs):
    today = now().date()

    # Get location from login POST (JS sends this)
    latitude = request.POST.get("latitude")
    longitude = request.POST.get("longitude")

    attendance, created = Attendance.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            "role": user.role,
            "login_time": now(),
            "latitude": latitude,
            "longitude": longitude,
            "status": "present",
            "marked_by": "system",
        }
    )

    # Safety: if record exists but login_time missing
    if not created and attendance.login_time is None:
        attendance.login_time = now()
        attendance.latitude = latitude
        attendance.longitude = longitude
        attendance.save()

    # Debug (optional – remove later)
    print("🔥 LOGIN SIGNAL FIRED FOR:", user.username)


@receiver(user_logged_out)
def mark_logout_attendance(sender, request, user, **kwargs):
    today = now().date()

    try:
        attendance = Attendance.objects.get(user=user, date=today)
        attendance.logout_time = now()
        attendance.save()
    except Attendance.DoesNotExist:
        pass
