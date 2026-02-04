from django.urls import path
from . import views

urlpatterns = [
    path("send/", views.send_message, name="send_message"),
    path("inbox/", views.inbox, name="inbox"),
    path("view/<int:pk>/", views.message_detail, name="message_detail"),
    path("reply/<int:pk>/", views.reply_message, name="reply_message"),
]
