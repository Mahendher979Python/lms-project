from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    date_of_joining = models.DateField(auto_now_add=True)
