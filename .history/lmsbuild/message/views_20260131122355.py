from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    # Logged in user ki vachina messages matrame
    inbox_messages = Message.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    return render(request, "message/inbox.html", {
        "messages": inbox_messages
    })


@login_required
def admin_send_message(request):

    # Role based user list
    if request.user.role == "trainer":
        users = User.objects.filter(role="student")

    elif request.user.role == "student":
        users = User.objects.filter(role="trainer")

    else:
        users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        receiver_id = request.POST.get("receiver")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        receiver = User.objects.get(id=receiver_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            body=body
        )

        # Success popup
        messages.success(request, "Message sent successfully!")

        # IMPORTANT: back to send page (not inbox)
        return redirect("send_message")

    return render(request, "message/admin/send.html", {
        "users": users
    })
