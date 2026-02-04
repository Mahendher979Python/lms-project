from django import forms
from django.contrib.auth import get_user_model

from .models import Student, TeacherProfile, StaffProfile

User = get_user_model()

# =====================================================
# USER FORM (COMMON)
# =====================================================
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'role',
            'mobile',
            'is_active'
        ]


# =====================================================
# TRAINER (TEACHER) PROFILE FORM
# =====================================================
class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = [
            'emp_id',
            'subject'
        ]


# =====================================================
# STAFF PROFILE FORM
# =====================================================
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = [
            'emp_id',
            'department',
            'position'
        ]


# =====================================================
# STUDENT CREATE FORM (ADMIN USE)
# =====================================================
class StudentCreateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 🔥 ADMIN assigns trainer here
    trainer = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.all()
    )

    class Meta:
        model = Student
        fields = [
            "roll_no",
            "phone",
            "trainer"
        ]


# =====================================================
# STUDENT UPDATE FORM
# =====================================================
class StudentUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = [
            "roll_no",
            "phone",
            "trainer"
        ]
