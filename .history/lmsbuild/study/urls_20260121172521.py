from django.urls import path
from . import views

urlpatterns = [
    # ADMIN TODO
    path("admin/todo/", views.admin_todo_list, name="admin_todo_list"),
    path("admin/todo/add/", views.admin_todo_add, name="admin_todo_add"),
    # TRAINER TODO
    path("trainer/todo/", views.trainer_todo_list, name="trainer_todo_list"),
    path("trainer/todo/add/", views.trainer_todo_add, name="trainer_todo_add"),
    # STUDENT TODO
    path("student/todo/", views.student_todo_list, name="student_todo_list"),

    # ADMIN NOTES
    path("admin/notes/", views.admin_notes_list, name="admin_notes_list"),
    path("admin/notes/add/", views.admin_notes_add, name="admin_notes_add"),
    path("admin/notes/edit/<int:pk>/", views.admin_notes_edit, name="admin_notes_edit"),
    path("admin/notes/delete/<int:pk>/", views.admin_notes_delete, name="admin_notes_delete"),

    # TRAINER NOTES
    path("trainer/notes/", views.trainer_notes_list, name="trainer_notes_list"),
    path("trainer/notes/add/", views.trainer_notes_add, name="trainer_notes_add"),
    path("trainer/notes/edit/<int:pk>/", views.trainer_notes_edit, name="trainer_notes_edit"),

    # STUDENT NOTES
    path("student/notes/", views.student_notes_list, name="student_notes_list"),


]
