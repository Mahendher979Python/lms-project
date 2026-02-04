from django.urls import path
from . import views

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("send/", views.admin_send_message, name="send_message"),
]
