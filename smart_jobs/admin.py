from django.contrib import admin
from smart_jobs.models import AppUser, Resumes, JobApplications, UserApplications, Recommendations

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Resumes)
admin.site.register(JobApplications)
admin.site.register(UserApplications)
admin.site.register(Recommendations)