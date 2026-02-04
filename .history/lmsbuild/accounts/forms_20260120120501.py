from django import forms
from .models import User, Student, TrainerProfile, TeacherProfile, StaffProfile
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'mobile', 'is_active']


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['emp_id', 'designation', 'experience']


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['emp_id', 'subject']


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['emp_id', 'department']



class StudentCreateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ["roll_no", "phone"]

class StudentUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    status = forms.ChoiceField(
        choices=(("active", "Active"), ("inactive", "Inactive"))
    )
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ["roll_no", "phone"]
