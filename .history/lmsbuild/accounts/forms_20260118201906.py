from django import forms
from .models import User


class AdminCreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        # role based flags
        if user.role == "admin":
            user.is_staff = True
            user.is_superuser = True
        elif user.role == "trainer":
            user.is_staff = True
            user.is_superuser = False
        else:  # student
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
