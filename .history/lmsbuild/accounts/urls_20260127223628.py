from django.urls import path
from . import views

urlpatterns = [

    # ================= AUTH =================
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # ================= DASHBOARDS =================
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    # ================= ADMIN → TRAINERS =================

    path("admin/trainers/", views.trainer_list, name="trainer_list"),

    path("admin/trainers/create/", views.admin_add_trainer, name="admin_add_trainer"),

    path("admin/trainers/<int:id>/edit/", views.admin_edit_trainer, name="admin_edit_trainer"),

    path("admin/trainers/<int:id>/delete/", views.trainer_delete, name="trainer_delete"),




    # ================= ADMIN → STUDENTS =================
    path("admin/students/", views.admin_students, name="admin_students"),
    path("admin/students/create/", views.admin_add_student, name="admin_add_student"),
    path("admin/students/<int:id>/edit/", views.admin_edit_student, name="admin_edit_student"),
    path("admin/students/<int:id>/delete/", views.admin_delete_student, name="admin_delete_student"),

   

    # ================= ADMIN → USERS =================
    path("admin/users/", views.admin_user_list, name="admin_user_list"),
    path("admin/users/<int:id>/", views.admin_user_view, name="admin_user_view"),
]
