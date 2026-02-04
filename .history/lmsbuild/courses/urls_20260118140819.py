from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('dashboard/trainer/courses/',views.trainer_course_list,name='trainer_course_list'),

]
