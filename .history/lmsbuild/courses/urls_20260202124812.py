from django.urls import path
from . import views

urlpatterns = [

# ==================================================
# ADMIN – COURSES
# ==================================================

path("admin/courses/", views.admin_course_list, name="admin_course_list"),
path("admin/courses/add/", views.admin_course_create, name="admin_course_create"),
path("admin/courses/<int:pk>/edit/", views.admin_course_edit, name="admin_course_edit"),
path("admin/courses/<int:pk>/delete/", views.admin_course_delete, name="admin_course_delete"),


# ==================================================
# ADMIN – MEDIA (VIDEOS)
# ==================================================

path("admin/media/", views.admin_media_list, name="admin_media_list"),
path("admin/media/upload/", views.admin_media_upload, name="admin_media_upload"),
path("admin/media/edit/<int:pk>/", views.admin_media_edit, name="admin_media_edit"),
path("admin/media/delete/<int:pk>/", views.admin_media_delete, name="admin_media_delete"),


# ==================================================
# ADMIN – MATERIALS (PDF + IMAGES)
# ==================================================

path("admin/materials/", views.admin_material_all_list, name="admin_material_all_list"),
path("admin/courses/<int:course_id>/materials/upload/", views.admin_material_upload, name="admin_material_upload"),
path("admin/materials/edit/<int:pk>/", views.admin_material_edit, name="admin_material_edit"),
path("admin/materials/<int:pk>/delete/", views.admin_material_delete, name="admin_material_delete"),


# ==================================================
# TRAINER – COURSES
# ==================================================

path("trainer/courses/", views.trainer_course_list, name="trainer_course_list"),
path("trainer/courses/<int:course_id>/preview/", views.trainer_course_preview, name="trainer_course_preview"),


# ==================================================
# TRAINER – MATERIALS
# ==================================================

path("trainer/materials/", views.trainer_material_redirect, name="trainer_material_redirect"),
path("trainer/courses/<int:course_id>/materials/", views.trainer_material_list, name="trainer_materials"),
path("trainer/courses/<int:course_id>/upload/", views.trainer_material_upload, name="trainer_material_upload"),
path("trainer/material/edit/<int:pk>/", views.trainer_material_edit, name="trainer_material_edit"),
path("trainer/material/delete/<int:pk>/", views.trainer_material_delete, name="trainer_material_delete"),


# ==================================================
# TRAINER – STUDENTS
# ==================================================

path("trainer/courses/<int:course_id>/students/", views.trainer_material_students, name="trainer_material_students"),
path("trainer/students/", views.trainer_students_redirect, name="trainer_students_redirect"),


# ==================================================
# STUDENT – COURSES
# ==================================================

path("student/courses/", views.student_course_list, name="student_course_list"),


# ==================================================
# STUDENT – MATERIALS
# ==================================================

path("student/materials/", views.student_material_redirect, name="student_material_redirect"),
path("student/materials/<int:course_id>/", views.student_material_list, name="student_material_list"),
path("student/material/<int:pk>/preview/", views.student_material_preview, name="student_material_preview"),

]
