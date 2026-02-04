from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Message

User = get_user_model()

@login_required
def admin_send_message(request):

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

        messages.success(request, "Message sent successfully!")
        return redirect("admin_send_message")

    return render(request,"message/admin/send.html",{
        "users":users
    })

@login_required
def inbox(request):

    msgs = Message.objects.filter(receiver=request.user).order_by("-created_at")

    return render(request,"message/inbox.html",{
        "messages":msgs
    })
