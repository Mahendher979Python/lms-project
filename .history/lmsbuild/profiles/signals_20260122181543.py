from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import StudentProfile, TrainerProfile, AdminProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "student":
        StudentProfile.objects.create(user=instance)

    elif instance.role == "trainer":
        TrainerProfile.objects.create(
            user=instance,
            qualification="",
            experience_years=0,
            expertise=""
        )

    elif instance.role in ["admin", "superadmin"]:
        AdminProfile.objects.create(user=instance)
