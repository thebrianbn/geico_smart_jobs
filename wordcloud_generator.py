from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import ast
import io

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geico_smart_jobs.settings")
import django
django.setup()
from smart_jobs.models import JobApplications
from django.core.files.images import ImageFile


def generate_word_cloud(tokens, job):

    all_words = ""
    for token in tokens:
        all_words = all_words + token + ' '

    stopwords = set(STOPWORDS)

    wc = WordCloud(width = 800, height = 800,
                   background_color='white',
                   stopwords=stopwords,
                   min_font_size = 10).generate(all_words)

    plot = plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)

    figure = io.BytesIO()
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    job.word_cloud = content_file
    job.save()


if __name__ == "__main__":

    job_apps = JobApplications.objects.all()
    for job in job_apps:
        tokens = ast.literal_eval(job.job_description)
        generate_word_cloud(tokens, job)