<<<<<<< HEAD
# Generated by Django 2.1.7 on 2019-03-17 09:01
=======
# Generated by Django 3.0.dev20190125164321 on 2019-03-17 07:30
>>>>>>> origin/master

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=25)),
                ('job_description', models.TextField()),
                ('job_description_words', models.TextField()),
                ('min_education', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='Recommendations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_jobs.JobApplications')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
=======
>>>>>>> origin/master
            name='Resumes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_name', models.CharField(max_length=25)),
                ('resume_file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('username', 'resume_name')},
            },
        ),
        migrations.CreateModel(
            name='UserApplications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=25, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='smart_jobs.JobApplications')),
                ('resume_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='smart_jobs.Resumes')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('username', 'job')},
            },
        ),
<<<<<<< HEAD
        migrations.AlterUniqueTogether(
            name='userapplications',
            unique_together={('username', 'job_title')},
        ),
        migrations.AlterUniqueTogether(
            name='resumes',
            unique_together={('username', 'resume_name')},
        ),
        migrations.AlterUniqueTogether(
            name='recommendations',
            unique_together={('username', 'job_title')},
=======
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_jobs.JobApplications')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('username', 'job')},
            },
>>>>>>> origin/master
        ),
    ]
