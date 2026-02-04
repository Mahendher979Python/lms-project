from django.urls import path

from lmsbuild.accounts import views
from .views import admin_settings_view, trainer_settings_view

urlpatterns = [
    path("admin/settings/", admin_settings_view, name="admin_settings"),
    path("admin/trainer-settings/", trainer_settings_view, name="trainer_settings"),
    path("admin/student-settings/",views.student_settings_view,name="student_settings"),

]
