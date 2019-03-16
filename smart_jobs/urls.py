from django.urls import path

from smart_jobs.views import JobBrowser, ResumeUpload

urlpatterns = [
    path('jobs/', JobBrowser.as_view(), name="job-browser")
    path('resume_upload/', ResumeUpload.as_view(), name="resume-upload")
]