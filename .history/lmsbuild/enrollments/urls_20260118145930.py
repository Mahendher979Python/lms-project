from django.urls import path
from . import views

urlpatterns = [
    # ✅ STUDENT COURSE LIST
    path(
        'dashboard/student/courses/',
        views.student_course_list,
        name='student_course_list'
    ),

    # ✅ COURSE DETAIL
    path(
        'dashboard/student/courses/<int:course_id>/',
        views.student_course_detail,
        name='student_course_detail'
    ),

    # ✅ ENROLL
    path(
        'dashboard/student/courses/<int:course_id>/enroll/',
        views.enroll_course,
        name='enroll_course'
    ),
]
