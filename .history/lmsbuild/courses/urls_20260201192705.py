from django.urls import path
from . import views

urlpatterns = [

    path("admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("admin/courses/add/", views.admin_course_create, name="admin_course_create"),
    path("admin/courses/<int:pk>/edit/", views.admin_course_edit, name="admin_course_edit"),
    path("admin/courses/<int:pk>/delete/", views.admin_course_delete, name="admin_course_delete"),

    # ADMIN MEDIA
    path("admin/media/", views.admin_media_list, name="admin_media_list"),
    path("admin/media/upload/", views.admin_media_upload, name="admin_media_upload"),
    path("admin/media/edit/<int:pk>/", views.admin_media_edit, name="admin_media_edit"),
    path("admin/media/delete/<int:pk>/",views.admin_media_delete,name="admin_media_delete"),

    # ADMIN MATERIALS
    path("admin/materials/",views.admin_material_all_list,name="admin_material_all_list"),
    path("admin/courses/<int:course_id>/materials/upload/",views.admin_material_upload,name="admin_material_upload"),   
    path("admin/materials/edit/<int:pk>/", views.admin_material_edit, name="admin_material_edit"),
    path("admin/materials/<int:pk>/delete/",views.admin_material_delete,name="admin_material_delete"),

    # TRAINER
    path("trainer/courses/", views.trainer_course_list, name="trainer_course_list"),
    path("trainer/courses/<int:course_id>/preview/",views.trainer_course_preview,name="trainer_course_preview"),
    path("trainer/courses/<int:course_id>/students/",views.trainer_students,name="trainer_students"),

    path("trainer/courses/<int:course_id>/upload/",views.trainer_material_upload,name="trainer_material_upload"),
    path("trainer/courses/<int:course_id>/materials/",views.trainer_material_list, name="trainer_materials"),

    path("trainer/material/delete/<int:pk>/", views.trainer_material_delete, name="trainer_material_delete"),

    path("student/courses/<int:course_id>/materials/",views.student_material_list,name="student_materials"),

]
