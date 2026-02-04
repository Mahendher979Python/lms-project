from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),


    path('admin/trainers/', trainer_list, name='trainer_list'),
    path('admin/trainers/create/', trainer_create, name='trainer_create'),
    path('admin/trainers/delete/<int:id>/', trainer_delete, name='trainer_delete'),

]
