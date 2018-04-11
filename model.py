"""Models and database for Job queue"""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; were getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the "session" object, where we do most of our interactions

DB_URI = "postgresql:///jobs"

# DB object
db = SQLAlchemy()



########################## Job Class ##########################################

class Job(db.Model):
    """Jobs in the job queue"""

    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    html = db.Column(db.String(), nullable=True)


    def __repr__(self):
        """Provides a helpful representation when a job is printed."""

        return "<Job ID = {} URL = {}".format(self.job_id, self.url)

######################### Helper functions ##################################### 

def connect_to_db(app, db_uri=DB_URI):
    """Connect the database to our Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    db.create_all()