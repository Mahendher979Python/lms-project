from django.urls import path
from . import views

urlpatterns = [
    path(
        'dashboard/student/courses/',
        views.student_course_list,
        name='student_course_list'
    ),
    path(
        'dashboard/student/courses/<int:course_id>/enroll/',
        views.enroll_course,
        name='enroll_course'
    ),
]
