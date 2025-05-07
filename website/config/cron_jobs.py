from pytz import timezone
from datetime import datetime
from sqlalchemy import and_, or_, not_, extract
from sqlalchemy.sql import func

manila_tz = timezone('Asia/Manila')

#add jobs here
def example_job(app, db):
    with app.app_context():
        
        #add a job logic here
        print('cron is running')
