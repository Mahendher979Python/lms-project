from accounts import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
]
