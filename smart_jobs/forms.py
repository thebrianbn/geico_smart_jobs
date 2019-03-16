from django import forms
from smart_jobs.models import Resumes


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resumes
        fields = ("resume_name", "resume_file", )
