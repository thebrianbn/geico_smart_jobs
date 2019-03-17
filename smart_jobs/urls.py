from django.urls import path

from smart_jobs.views import JobBrowser, ResumeUpload, Home, RecommendationsView, JobApplicationDetail, \
    Dashboard

urlpatterns = [
    path('jobs/', JobBrowser.as_view(), name="job-browser"),
    path('resume_upload/', ResumeUpload.as_view(), name="resume-upload"),
    path('', Home.as_view(), name="home"),
    path('recommendations/', RecommendationsView.as_view(), name="recommendations"),
    path('jobs/<int:pk>/', JobApplicationDetail.as_view(), name="job-detail"),
    path('dashboard/', Dashboard.as_view(), name="dashboard")
]