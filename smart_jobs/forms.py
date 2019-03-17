from django import forms
from smart_jobs.models import Resumes
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resumes
        fields = ("resume_name", "resume_file", )

<<<<<<< HEAD
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']
=======

class BlankForm(forms.Form):
    pass
>>>>>>> origin/master
