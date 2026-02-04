
from django.urls import path
from core_settings import views

urlpatterns = [

    # ================= ADMIN SETTINGS =================
    path(
        "admin/settings/",
        views.admin_settings_view,
        name="admin_settings"
),

    path(
        "admin/trainer-settings/",
        views.trainer_settings_view,
        name="trainer_settings"
    ),

    path(
        "admin/student-settings/",
        views.student_settings_view,
        name="student_settings"
    ),
]
