from django.shortcuts import render, redirect
from django.views.generic import View

from smart_jobs.models import Resumes
from smart_jobs.forms import ResumeForm


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