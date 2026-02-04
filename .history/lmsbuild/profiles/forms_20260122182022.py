from django import forms
from .models import StudentProfile, TrainerProfile, AdminProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"
        exclude = ["user"]


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = "__all__"
        exclude = ["user", "rating", "is_approved"]


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = "__all__"
        exclude = ["user"]
