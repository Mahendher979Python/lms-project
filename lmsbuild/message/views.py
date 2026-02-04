from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    msgs = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by("created_at")

    return render(request, "message/inbox.html", {"messages": msgs})


@login_required
def send_message(request):

    if request.user.role == "trainer":
        users = User.objects.filter(role="student")
    elif request.user.role == "student":
        users = User.objects.filter(role="trainer")
    else:
        users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        receiver = User.objects.get(id=request.POST["receiver"])

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=request.POST["subject"],
            body=request.POST["body"]
        )

        messages.success(request, "Message sent successfully!")
        return redirect("send_message")

    return render(request, "message/admin/send.html", {"users": users})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, id=pk)

    if msg.receiver == request.user:
        msg.is_read = True
        msg.save()

    return render(request, "message/admin/detail.html", {"msg": msg})


@login_required
def reply_message(request, pk):
    original = get_object_or_404(Message, id=pk)

    if request.method == "POST":
        Message.objects.create(
            sender=request.user,
            receiver=original.sender,
            subject="Re: " + original.subject,
            body=request.POST["body"]
        )
        return redirect("inbox")

    return render(request, "message/admin/reply.html", {"msg": original})
