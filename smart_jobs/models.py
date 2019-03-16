from django.db import models
from django.contrib.auth.models import User


class AppUser(User):

    position_preference = models.CharField(max_length=50, null=True)
    education = models.CharField(max_length=50, null=True)
    image = models.ImageField(null=True)


class Resumes(models.Model):

    resume_name = models.CharField(max_length=25)
    resume_file = models.FileField()
    username = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:

        unique_together = (("username", "resume_name"),)


class JobApplications(models.Model):

    job_title = models.CharField(max_length=25, primary_key=True)
    job_description = models.TextField()
    min_education = models.CharField(max_length=50, null=True)


class UserApplications(models.Model):

    username = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobApplications, on_delete=models.DO_NOTHING)
    resume_name = models.ForeignKey(Resumes, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=25, null=True)

    class Meta:

        unique_together = (("username", "job_title"),)


class Recommendations(models.Model):

    username = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobApplications, on_delete=models.CASCADE)

    class Meta:

        unique_together = (("username", "job_title"),)