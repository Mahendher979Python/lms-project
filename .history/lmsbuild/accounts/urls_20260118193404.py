from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 🚫 DO NOT use admin/
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
]
