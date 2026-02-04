from django.urls import path
from . import views

urlpatterns = [
    path("admin/todo/", views.admin_todo_list, name="admin_todo_list"),
    path("admin/todo/add/", views.admin_todo_add, name="admin_todo_add"),

    # TRAINER
path("trainer/todo/", views.trainer_todo_list, name="trainer_todo_list"),
path("trainer/todo/add/", views.trainer_todo_add, name="trainer_todo_add"),
    # STUDENT
    path("student/todo/", views.student_todo_list, name="student_todo_list"),
    

]
