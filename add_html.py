from python import requests

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger



scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=print_date_time,
    trigger=IntervalTrigger(seconds=5),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def get_html(requested_url):
    """Gets HTML from the requested URL"""

    # Query for the job filtered by the job id that has been passed in
    # Update the job's html field in the database

    r = requests.get(requested_url)
    html = r.text

    return html


def add_html_to_db(job_id, html):
    """Adds HTMl to the database"""

    # We can use one becuase the job will definitly be in the database
    # once and only once
    job = Job.query.filter(Job.job_id == job_id).one()

    job.html = html

    db.session.commit()





