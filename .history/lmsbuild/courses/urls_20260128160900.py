from django.urls import path
from . import views

urlpatterns = [

    # ADMIN COURSES
    path("admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("admin/courses/create/", views.admin_course_create, name="admin_course_create"),
    path("admin/courses/edit/<int:pk>/", views.admin_course_edit, name="admin_course_edit"),
    path("admin/courses/delete/<int:pk>/", views.admin_course_delete, name="admin_course_delete"),
]
