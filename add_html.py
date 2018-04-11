import requests


# theres DB query to get jobs where HTML is Null
# for each of these jobs, we will get the URL field
# now we will go this URL, get the response HTML
# Then we update the Jobs HTML field with this information and save to DB

def update_html_in_database():
    """Updates the HTML in the database"""

    null_jobs = Job.query.filter(Job.html == None)
    print null_jobs

    

def get_html(requested_url):
    """Gets HTML from the requested URL"""

    # Query for the job filtered by the job id that has been passed in
    # Update the job's html field in the database

    r = requests.get(requested_url)
    html = r.text

    print html

    return html


def add_html_to_db(job_id, html):
    """Adds HTMl to the database"""

    # We can use one becuase the job will definitly be in the database
    # once and only once
    job = Job.query.filter(Job.job_id == job_id).one()

    job.html = html

    db.session.commit()

