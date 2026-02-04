from django import forms
from .models import StudentProfile, TrainerProfile, AdminProfile
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()



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



class UserProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["profile_pic"]