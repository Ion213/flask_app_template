from website import flask_app
from website.config.modules import db
from website.config.cron_jobs import example_job

def cron_run(app, db):
    example_job(app, db)

if __name__ == "__main__":
    app = flask_app()  # Initialize the Flask app
    with app.app_context():  # Ensure we run the cron jobs inside the app context
        cron_run(app, db)  # Run the cron jobs