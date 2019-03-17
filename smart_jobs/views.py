from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from smart_jobs.models import Resumes, JobApplications, AppUser
from smart_jobs.forms import ResumeForm

from django.contrib.auth.forms import UserCreationForm
from django import forms


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
        else:
            render(request, "hello")
        return redirect('register')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")

    class Meta:
        model = AppUser
        fields = ("username", "first_name", "last_name", "email", )

class ResumeUpload(View):

    def get(self, request):

        form = ResumeForm()
        return render(request, "#", {"form": form})

    def post(self, request):

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Update associated user to resume
            new_resume = Resumes.objects.get(form.id)
            new_resume.username = request.user
            return redirect('home')

        return render(request, "#", )


class JobBrowser(ListView):

    def get(self, request):
        job_apps = JobApplications.objects.all()

        return render(request, "browser.html", {"job_apps": job_apps})

    def post(self, request):

        pass
