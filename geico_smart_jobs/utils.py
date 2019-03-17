from heapq import nlargest
from smart_jobs.models import JobApplications
from parse_docx import parse_docx



def get_matches(path):

    doc = path

    new_tokens = parse_docx(doc)

    jobs = JobApplications.objects.all()

    match_dict = {}
    for job in jobs:
        tmp = ''.join(c for c in job.job_description if c not in "[]',")

        match_count = 0
        for word in tmp.split(" "):

            if word in new_tokens:
                match_count += 1

        title = job.job_title
        for word in title.split(" "):
            word = word.strip('()')
            word = word.lower()
            if word in new_tokens:
                match_count += 5
        match_dict[job.id] = match_count

    five = nlargest(5, match_dict, key=match_dict.get)
    return five


