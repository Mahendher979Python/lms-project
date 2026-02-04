from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    inbox_messages = Message.objects.filter(receiver=request.user).order_by("-created_at")
    return render(request, "message/inbox.html", {"messages": inbox_messages})


@login_required
def admin_send_message(request):
    # If trainer → show students
    if request.user.role == "trainer":
        users = User.objects.filter(role="student")

    # If student → show trainers
    elif request.user.role == "student":
        users = User.objects.filter(role="trainer")

    else:
        users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        receiver = User.objects.get(id=request.POST.get("receiver"))
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            body=body
        )

        return redirect("inbox")

    return render(request, "message/admin/send.html", {"users": users})
