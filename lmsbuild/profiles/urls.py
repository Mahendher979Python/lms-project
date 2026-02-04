from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="profile_view"),

    # ADMIN URLs
    path("admin/students/", views.admin_student_list, name="admin_student_list"),
    path("admin/trainers/", views.admin_trainer_list, name="admin_trainer_list"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("admin/<str:role>/<int:profile_id>/",views.admin_profile_detail, name="admin_profile_detail",),
]
