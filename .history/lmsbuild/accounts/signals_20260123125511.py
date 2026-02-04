from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Student, TeacherProfile, StaffProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_role_based_profile(sender, instance, created, **kwargs):
    """
    Auto create profile based on user role
    """

    if not created:
        return

    # =========================
    # TRAINER
    # =========================
    if instance.role == "trainer":
        TeacherProfile.objects.create(
            user=instance,
            emp_id=f"TRN-{instance.id}",
            subject="Not Assigned"
        )

    # =========================
    # STUDENT
    # =========================
    elif instance.role == "student":
        # Student profile is NOT auto-created here
        # Because trainer assignment is REQUIRED
        pass

    # =========================
    # STAFF
    # =========================
    elif instance.role == "staff":
        StaffProfile.objects.create(
            user=instance,
            emp_id=f"STF-{instance.id}",
            department="General",
            position="Staff"
        )
