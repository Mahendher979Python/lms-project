from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        print(
            f"New message from {instance.sender} to {instance.receiver}"
        )
