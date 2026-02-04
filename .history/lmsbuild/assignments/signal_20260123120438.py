from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission, Certificate


@receiver(post_save, sender=Submission)
def create_certificate_on_pass(sender, instance, created, **kwargs):
    """
    Auto-generate certificate when student passes assignment
    """

    if instance.status == "submitted":
        assignment = instance.assignment

        if instance.score >= assignment.pass_marks:
            Certificate.objects.get_or_create(
                submission=instance
            )
