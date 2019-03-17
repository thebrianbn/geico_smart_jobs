from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.core.mail import send_mail

from smart_jobs.models import Resumes, JobApplications, User, Recommendations, UserApplications
from smart_jobs.forms import ResumeForm, BlankForm

from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django import forms
from django.utils.decorators import method_decorator
from geico_smart_jobs.utils import get_matches

import ast


class Home(View):

    def get(self, request):

        return render(request, "home.html", {"title": "Home"})

    def post(self, request):

        return render(request, "home.html", {"title": "Home"})


class Register(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form, 'title': 'registration'})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
        return redirect('login')


class Profile(View):

    def post(self, request):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('profile')

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'title': 'Profile'
        }
        return render(request, 'profile.html', context)


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    education = forms.CharField(label="Education level")
    position_preference = forms.CharField(label="Position preference")
    location_preference = forms.CharField(label="Position preference")

    class Meta:
        fields = (
        "username", "first_name", "last_name", "email", "education", "position_preference", "location_preference")

        
class ResumeUpload(View):

    def get(self, request):

        form = ResumeForm()
        return render(request, "resume_upload.html", {"form": form, 'title': 'Resume Upload'})

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

        return render(request, "resume_upload.html", {'title': 'Resume Upload'})


class JobBrowser(ListView):

    model = JobApplications

    def get(self, request):
        job_apps = JobApplications.objects.all()
        new_apps = []
        for app in job_apps:
            app.job_description = ast.literal_eval(app.job_description)[:10]
            new_apps.append(app)

        return render(request, "browser.html", {"job_apps": new_apps, "title": "GEICO Jobs"})

    def post(self, request):
        return redirect("job-browser")


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

        return redirect("job-browser")


class RecommendationsView(View):

    def get(self, request):

        job_apps = []
        reccs = Recommendations.objects.filter(username=request.user)
        for rec in reccs:
            job_apps.append(rec.job)

        return render(request, "browser.html", {"job_apps": job_apps, "title": "Your Recommendations"})

    def post(self, request):
        return render(request, "browser.html")


class Dashboard(View):

    def get(self, request):
        context = {}
        apps = UserApplications.objects.filter(username=request.user)
        context["apps"] = apps
        context["title"] = "User Dashboard"
        return render(request, "user_dashboard.html", context=context)

    def post(self, request):
        pass