from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from smart_jobs.models import Resumes, JobApplications, User, Recommendations
from smart_jobs.forms import ResumeForm

from django.contrib.auth.forms import UserCreationForm
from django import forms
from geico_smart_jobs.utils import get_matches

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
        return redirect('home')

class Profile(View):

    def get(self, request):
        return render(request, 'profile.html')


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
            new_resume.save()

            matches = get_matches(new_resume.resume_file)
            for match in matches:

                job_app = JobApplications.objects.get(job_title=match)
                match_exists = Recommendations.objects.filter(username=request.user, job_title=job_app).count() == 1
                if not match_exists:
                    new_match = Recommendations(job_title=job_app, username=request.user)
                    new_match.save()

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


class JobApplication(View):

    pass


class RecommendationsView(View):

    def get(self, request):

        job_apps = []
        reccs = Recommendations.objects.filter(username=request.user)
        for rec in reccs:
            job_apps.append(JobApplications.objects.get(job_title=rec.job_title))

        return render(request, "browser.html", {"job_apps": job_apps})

    def post(self, request):
        return render(request, "browser.html")

