from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from smart_jobs.models import Resumes, JobApplications, User
from smart_jobs.forms import ResumeForm

from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django import forms
from django.utils.decorators import method_decorator

class Home(View):

    def get(self, request):

        return render(request, "home.html")

    def post(self, request):

        return render(request, "home.html")


class Register(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
        return redirect('login')

class Profile(View):

    def get(self, request):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'profile.html', context)


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")

    class Meta:
        fields = ("username", "first_name", "last_name", "email", )

class ResumeUpload(View):

    def get(self, request):

        form = ResumeForm()
        return render(request, "resume_upload.html", {"form": form})

    def post(self, request):

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Update associated user to resume
            new_resume = Resumes.objects.latest("id")
            new_resume.username = request.user
            return render(int(request.user))
            new_resume.save()
            return redirect('home')
        else:
            render(request, "hello")

        return render(request, "resume_upload.html")


class JobBrowser(ListView):

    def get(self, request):
        job_apps = JobApplications.objects.all()

        return render(request, "browser.html", {"job_apps": job_apps})

    def post(self, request):
        return render(request, "browser.html")
