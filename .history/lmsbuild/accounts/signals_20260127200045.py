from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import TeacherProfile, Student, StaffProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_and_assign_group(sender, instance, created, **kwargs):
    if not created:
        return

    # -------------------------------
    # GROUP AUTO ASSIGN
    # -------------------------------
    if instance.role:
        group, _ = Group.objects.get_or_create(
            name=instance.role.capitalize()
        )
        instance.groups.add(group)

    # -------------------------------
    # TRAINER PROFILE
    # -------------------------------
    if instance.role == "trainer":
        TeacherProfile.objects.get_or_create(
            user=instance,
            defaults={
                "emp_id": f"TRN-{instance.id}",
                "subject": "Not Assigned"
            }
        )

    # -------------------------------
    # STAFF PROFILE
    # -------------------------------
    elif instance.role == "staff":
        StaffProfile.objects.get_or_create(
            user=instance,
            defaults={
                "emp_id": f"STF-{instance.id}",
                "department": "General",
                "position": "Staff"
            }
        )

    # -------------------------------
    # STUDENT PROFILE
    # -------------------------------
    elif instance.role == "student":
        # Student created manually because trainer + batch required
        pass
