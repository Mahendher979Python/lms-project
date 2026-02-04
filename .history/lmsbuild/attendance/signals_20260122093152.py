from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Attendance


@receiver(pre_save, sender=Attendance)
def calculate_work_hours_signal(sender, instance, **kwargs):
    """
    Automatically calculate total work hours
    whenever login_time and logout_time are available
    """
    if instance.login_time and instance.logout_time:
        instance.total_work_hours = (
            instance.logout_time - instance.login_time
        )
    else:
        instance.total_work_hours = None
