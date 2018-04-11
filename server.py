import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from flask import Flask, request, jsonify
from model import db, connect_to_db, Job

from add_html import update_html_in_database

import logging


# We need to create our flask application
# Flask needs to know what module to scan for things like routes
# So the __name__ is required

app = Flask(__name__)


####################### Will run if we start our server########################


# This decorator will run functions that should be called at the begginging
# Of the first request

@app.before_first_request
def initialize_background_job():
    """Runs update html in the database function every three seconds in background"""

    ####### Found on stack overflow to fix a logging error  ####### 
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    #####################################################################
    # Background scheduler runs the function update html in the database every 3 seconds

    scheduler = BackgroundScheduler()
    scheduler.add_job(update_html_in_database, 'interval', seconds=3)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


@app.route('/', methods=['POST'])
def create_job():
    """Creates a job in the database and returns the job ID to the user"""

    # Get the URL back from the form
    # Query the database to get the URL back
    # If the URl is not in the table, add it to the table, get job ID
    # If the URL is in the table already, get the Job ID
    # Return the job ID to the user as JSON

    requested_url = request.form.get("url")

    url = Job.query.filter(Job.url == requested_url).first()

    if not url:
        url = Job(url=requested_url)
        db.session.add(url)
        db.session.commit()

    job_id = url.job_id

    job_details = {"job_id": job_id}

    return jsonify(job_details)


@app.route('/<int:job_id>')
def get_html(job_id):
    """Gets the HTML back from a job in the database"""

    # Get the job id from the URL
    # Query for the HTMl filtered by job id
    # If there is html, send it as JSON to the user
    # If there isn't html, send a message to the user saying
    # HTML is not ready yet

    job = Job.query.filter(Job.job_id == job_id).first()

    html = job.html

    if html:
        job_details = {"html": html}
    else:
        job_details = {"message": "The HTML for this page is not ready yet"}


    return jsonify(job_details)



####################### Will Run if we Run our Server ###########################

if __name__ == "__main__":
    # Connect our flask app to the DB
    connect_to_db(app)
    # Run our flask app on our local machine
    app.run(host="0.0.0.0")

