from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),



path('dashboard/trainers/', views.trainer_list, name='trainer_list'),
path('dashboard/trainers/create/', views.trainer_create, name='trainer_create'),
path('dashboard/trainers/edit/<int:id>/', views.trainer_edit, name='trainer_edit'),
path('dashboard/trainers/delete/<int:id>/', views.trainer_delete, name='trainer_delete'),
]

