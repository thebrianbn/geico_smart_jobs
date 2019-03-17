from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.core.mail import send_mail

from smart_jobs.models import Resumes, JobApplications, User, Recommendations, UserApplications
from smart_jobs.forms import ResumeForm, BlankForm

from django.contrib.auth.forms import UserCreationForm
from django import forms
from geico_smart_jobs.utils import get_matches


class Home(View):

    def get(self, request):

        return render(request, "home.html", {"title": "Home"})

    def post(self, request):

        return render(request, "home.html", {"title": "Home"})


class Register(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Registration successful.")
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

                job_app = JobApplications.objects.get(id=match)
                match_exists = Recommendations.objects.filter(username=request.user, id=job_app.id).count() == 1
                if not match_exists:
                    new_match = Recommendations(job=job_app, username=request.user)
                    new_match.save()

            return redirect('home')
        else:
            render(request, "hello")

        return render(request, "resume_upload.html")


class JobBrowser(ListView):

    model = JobApplications

    def get(self, request):
        job_apps = JobApplications.objects.all()

        return render(request, "browser.html", {"job_apps": job_apps, "title": "GEICO Jobs"})

    def post(self, request):
        return render(request, "browser.html")


class JobApplicationDetail(DetailView):

    model = JobApplications
    template_name = "job_detail.html"

    def post(self, request, pk):

        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to apply to any position.")
            return redirect("home")

        job = JobApplications.objects.get(id=pk)
        application_exists = UserApplications.objects.filter(username=request.user, job=job).count() == 1

        if not application_exists:
            resume = Resumes.objects.filter(username=request.user).latest("id")
            new_application = UserApplications(username=request.user, job=job, status="Applied", resume_name=resume)
            new_application.save()
            messages.success(request, "Applied to job successfully.")
        else:
            messages.error(request, "You have already applied to this job.")

        return redirect("home")


class RecommendationsView(View):

    def get(self, request):

        job_apps = []
        reccs = Recommendations.objects.filter(username=request.user)
        for rec in reccs:
            job_apps.append(rec.job)

        return render(request, "browser.html", {"job_apps": job_apps, "title": "Your Recommendations"})

    def post(self, request):
        return render(request, "browser.html")

