from django.urls import path
from . import views

urlpatterns = [
    path("admin/todo/", views.admin_todo_list, name="admin_todo_list"),
    path("admin/todo/add/", views.admin_todo_add, name="admin_todo_add"),
]
