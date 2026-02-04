from django.db import models
from django.contrib.auth.models import User
from courses.models import Batch

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)

    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
