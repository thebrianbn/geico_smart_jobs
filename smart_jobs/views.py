from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from smart_jobs.models import Resumes, JobApplications, User
from smart_jobs.forms import ResumeForm

from django.contrib.auth.forms import UserCreationForm
from django import forms


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
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
        return redirect('register')


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
