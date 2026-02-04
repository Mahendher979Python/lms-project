from django.urls import path
from . import views

urlpatterns = [
    # ================= ADMIN COURSE ===============================================CRUD
    path("admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("admin/courses/add/", views.admin_course_create, name="admin_course_create"),
    path("admin/courses/<int:pk>/edit/", views.admin_course_edit, name="admin_course_edit"),
    path("admin/courses/<int:pk>/delete/", views.admin_course_delete, name="admin_course_delete"),

    # ================= ADMIN MEDIA =========================================================CRUD
    path("admin/media/", views.admin_media_list, name="admin_media_list"),
    path("admin/media/upload/", views.admin_media_upload, name="admin_media_upload"),
    path("admin/media/edit/<int:material_id>/",views.admin_media_edit,name="admin_media_edit"),
    path("admin/media/delete/<int:material_id>/",views.admin_media_delete,name="admin_media_delete"),


    # ================= ADMIN MATERIAL ====================================================CRUD
    path("admin/courses/<int:course_id>/materials/", views.admin_material_list, name="admin_material_list"),
    path("admin/courses/<int:course_id>/materials/upload/", views.admin_material_upload, name="admin_material_upload"),
    path("admin/materials/edit/<int:material_id>/",views.admin_material_edit,name="admin_material_edit"),
    path("admin/materials/<int:material_id>/delete/", views.admin_material_delete, name="admin_material_delete"),

    # ================= TRAINER MATERIAL =============================================CRU



    # ================= TRAINER COURSES =================
    path("trainer/courses/",views.trainer_courses,name="trainer_courses"),
    path("trainer/course/<int:course_id>/students/",views.trainer_students,name="trainer_students"),

    # STUDENT MATERIALS VIEWS
    path("student/materials/<int:batch_id>/",views.student_materials,name="student_materials"),


]



