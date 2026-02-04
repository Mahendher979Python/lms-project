from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role:
        group, _ = Group.objects.get_or_create(name=instance.role.capitalize())
        instance.groups.add(group)
