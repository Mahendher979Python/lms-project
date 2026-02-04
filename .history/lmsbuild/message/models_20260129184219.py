from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Message(models.Model):

    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent")

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received"
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    subject = models.CharField(max_length=200)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
