import ast
import json
from nltk.corpus import stopwords
import os

# Set up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geico_smart_jobs.settings")
import django
django.setup()
from smart_jobs.models import JobApplications


def load_jobs():

    with open("articles2.json", "r") as f:
        articles = ast.literal_eval(f.read())
        counter = 0
        for article in articles:
            min_education = article["min_education"]
            job_title = article["job_title"][:-16]
            location = article["location"]

            stop_words = stopwords.words("english")
            filtered_description = []

            # get rid of footer words
            job_description = article["job_description"]

            if len(job_description) < 24:
                continue

            job_description = job_description[1:-23]
            new_description = [list(filter(str.isalnum, x.split())) for x in job_description]
            new_description = [keyword.lower() for x in new_description for keyword in x]

            for word in new_description:
                if word not in stop_words:
                    filtered_description.append(word)

            new_job_app = JobApplications(min_education=min_education, job_title=job_title,
                                          job_description=filtered_description, location=location)

            new_job_app.save()



if __name__ == "__main__":

    load_jobs()