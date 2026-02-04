from django.urls import path
from . import views


urlpatterns = [
    # ADMIN – COURSES
    path("admin/courses/", views.admin_course_list, name="admin_course_list"),
    path("admin/courses/add/", views.admin_course_add, name="admin_course_add"),
    path("admin/courses/edit/<int:course_id>/", views.admin_course_edit, name="admin_course_edit"),
    path("admin/courses/delete/<int:course_id>/", views.admin_course_delete, name="admin_course_delete"),



    # =========================
    # TRAINER – COURSES
    # =========================
    path("trainer/courses/", views.trainer_course_list, name="trainer_course_list"),
    path("trainer/courses/add/", views.trainer_course_create, name="trainer_course_create"),
    path("trainer/courses/edit/<int:course_id>/", views.trainer_course_edit, name="trainer_course_edit"),

    # =========================
    # TRAINER – LESSONS
    # =========================
    path("trainer/courses/<int:course_id>/lessons/",views.trainer_lesson_list,name="trainer_lesson_list"),
    path("trainer/courses/<int:course_id>/lessons/add/",views.trainer_lesson_add, name="trainer_lesson_add"),
    path("trainer/courses/<int:course_id>/lessons/edit/<int:lesson_id>/",views.trainer_lesson_edit,name="trainer_lesson_edit"),
    path("trainer/courses/<int:course_id>/lessons/delete/<int:lesson_id>/",views.trainer_lesson_delete,name="trainer_lesson_delete"),

    # =========================
    # PUBLIC – MEDIA
    # =========================
    path("media/", views.public_media_view, name="public_media_view"),

    # =========================
    # ADMIN – MEDIA
    # =========================
    path("admin/media/", views.admin_media_list, name="admin_media_list"),

    # =========================
    # TRAINER – MEDIA DASHBOARD
    # =========================
    path("trainer/media/", views.trainer_media_list, name="trainer_media_list"),

    # =========================
    # TRAINER – VIDEOS CRUD
    # =========================

    path("trainer/videos/", views.trainer_video_list, name="trainer_video_list"),
    path("trainer/videos/add/", views.trainer_video_add, name="trainer_video_add"),
    path("trainer/videos/edit/<int:video_id>/", views.trainer_video_edit, name="trainer_video_edit"),
    path("trainer/videos/delete/<int:video_id>/", views.trainer_video_delete, name="trainer_video_delete"),

    # =========================
    # STUDENT VIEWS
    # =========================
    path("student/courses/", views.student_course_list,name="student_course_list"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/course/<int:course_id>/", views.student_course_detail, name="student_course_detail"),
    path("student/course/<int:course_id>/lessons/", views.student_lesson_list, name="student_lesson_list"),


    path(
        "student/my-courses/",
        views.student_my_courses,
        name="student_my_courses"
    ),

    path(
        "student/course/<int:course_id>/topics/",
        views.student_course_topics,
        name="student_course_topics"
    ),

    path(
        "student/course/<int:course_id>/download/",
        views.download_course,
        name="download_course"
    ),


    # =========================
    # TRAINER – ADS / IMAGES CRUD
    # =========================
    path("trainer/ads/", views.trainer_ad_list, name="trainer_ad_list"),
    path("trainer/ads/add/", views. trainer_ad_add, name="trainer_ad_add"),
    path("trainer/ads/edit/<int:ad_id>/", views.trainer_ad_edit, name="trainer_ad_edit"),
    path("trainer/ads/delete/<int:ad_id>/",views. trainer_ad_delete, name="trainer_ad_delete"),


]
