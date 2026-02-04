from django.urls import path
from . import views

urlpatterns = [

    # ADMIN COURSES
    path("admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("admin/courses/create/", views.admin_course_create, name="admin_course_create"),
    path("admin/courses/edit/<int:pk>/", views.admin_course_edit, name="admin_course_edit"),
    path("admin/courses/delete/<int:pk>/", views.admin_course_delete, name="admin_course_delete"),

    # TRAINER MATERIALS
    path("trainer/courses/<int:course_id>/materials/", views.trainer_material_list, name="trainer_material_list"),
    path("trainer/courses/<int:course_id>/materials/upload/", views.trainer_material_upload, name="trainer_material_upload"),

    # Media
    path("admin/media/", views.admin_media_list, name="admin_media_list"),
    path("admin/media/upload/", views.admin_media_upload, name="admin_media_upload"),

   # Courses
    path("trainer/courses/", views.trainer_course_list, name="trainer_course_list"),

]
