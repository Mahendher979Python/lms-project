from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('dashboard/trainer/courses/',views.trainer_course_list,name='trainer_course_list'),
    path('dashboard/trainer/courses/add/',views.trainer_course_create,name='trainer_course_add'),
    path('dashboard/trainer/courses/<int:course_id>/edit/',views.trainer_course_edit,name='trainer_course_edit'),


]
