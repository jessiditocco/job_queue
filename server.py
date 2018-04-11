from flask import Flask, request, jsonify
from model import db, connect_to_db, Job

# We need to create our flask application
# Flask needs to know what module to scan for things like routes
# So the __name__ is required

app = Flask(__name__)



####################### Will run if we start our server########################

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

    print "This is the job id!!!", job_id

    job = Job.query.filter(Job.job_id == job_id).first()
    print "This is the Job!!!!!", job

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

