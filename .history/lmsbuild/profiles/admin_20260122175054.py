.
from django.contrib import admin
from .models import StudentProfile, TrainerProfile, AdminProfile

admin.site.register(StudentProfile)
admin.site.register(TrainerProfile)
admin.site.register(AdminProfile)
