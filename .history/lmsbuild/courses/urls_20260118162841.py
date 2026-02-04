from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('dashboard/trainer/courses/',views.trainer_course_list,name='trainer_course_list'),
    path('dashboard/trainer/courses/add/',views.trainer_course_create,name='trainer_course_add'),
    path('dashboard/trainer/courses/<int:course_id>/edit/',views.trainer_course_edit,name='trainer_course_edit'),
    path('dashboard/trainer/courses/<int:course_id>/lessons/',views.trainer_lesson_list,name='trainer_lesson_list'),
    path('dashboard/trainer/courses/<int:course_id>/lessons/add/',views.trainer_lesson_add,name='trainer_lesson_add'),

    path(
    'media/',
    views.public_media_view,
    name='public_media'
),

path(
    'dashboard/admin/media/',
    views.admin_media_list,
    name='admin_media_list'
),

# trainer urls
# Trainer Media
path("trainer/videos/", trainer_video_list, name="trainer_video_list"),
path("trainer/videos/add/", trainer_video_add, name="trainer_video_add"),
path("trainer/videos/edit/<int:video_id>/", trainer_video_edit, name="trainer_video_edit"),
path("trainer/videos/delete/<int:video_id>/", trainer_video_delete, name="trainer_video_delete"),

path("trainer/ads/", trainer_ad_list, name="trainer_ad_list"),
path("trainer/ads/add/", trainer_ad_add, name="trainer_ad_add"),
path("trainer/ads/edit/<int:ad_id>/", trainer_ad_edit, name="trainer_ad_edit"),
path("trainer/ads/delete/<int:ad_id>/", trainer_ad_delete, name="trainer_ad_delete"),

]
