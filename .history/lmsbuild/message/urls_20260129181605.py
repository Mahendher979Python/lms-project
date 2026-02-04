from django.urls import path
from . import views

urlpatterns = [
    path("admin/messages/send/", views.admin_send_message, name="admin_send_message"),
    path("messages/inbox/", views.inbox, name="inbox"),

]