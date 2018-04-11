import requests
from model import db, Job

# Make a DB query to get jobs where HTML is Null
# Loop through each of these jobs; we will get the URL field
# now we will go this URL, get the response HTML
# Then we update the Jobs HTML field with this information and save to DB

def update_html_in_database():
    """Updates the HTML in the database in the background"""

    null_jobs = Job.query.filter(Job.html == None).all()

    for job in null_jobs:
        url = job.url

        r = requests.get(url)
        html = r.text

        job.html = html

        print "Succesfully updated the html for job # {} in the database".format(job.job_id)

        db.session.commit()

