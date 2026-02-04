
from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # DASHBOARDS
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    # ADMIN – TRAINERS
    path("admin/trainers/", views.trainer_list, name="trainer_list"),
    path("admin/trainers/create/", views.trainer_create, name="trainer_create"),
    path("admin/trainers/<int:id>/delete/", views.trainer_delete, name="trainer_delete"),

    # ADMIN – STUDENTS
    path("admin/students/", views.admin_students, name="admin_students"),
    path("admin/students/add/", views.admin_add_student, name="admin_add_student"),
    path("admin/students/created/", views.admin_student_created, name="admin_student_created"),
    path("admin/students/<int:id>/edit/", views.admin_edit_student, name="admin_edit_student"),
    path("admin/students/<int:id>/delete/", views.admin_delete_student, name="admin_delete_student"),

    # TRAINER – STUDENTS
    path("trainer/students/", views.trainer_students, name="trainer_students"),")


    path('dashboard/trainers/edit/<int:id>/', views.trainer_edit, name='trainer_edit'),
    path("admin/users/", views.admin_user_list, name="admin_user_list"),
    path("admin/users/<int:id>/", views.admin_user_view, name="admin_user_view"),


]
