import os
from pytz import timezone
from datetime import timedelta, datetime
from flask_login import current_user

from website.config.modules import (
    db,
    login_manager
)

from website.config.env_loader import (
    database_url,
    GMAIL,
    PASSWORD,
    SECRET_KEY
)


DB_NAME = "sqlite.db"
manila_tz = timezone('Asia/Manila')

# Configuration function for Flask app
def database_config(app): 
    # Set database URI
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        print("⚠️  DATABASE_URL is not set. Using SQLite instead.")
        db_path = os.path.join(app.root_path, 'sqlite_db', DB_NAME)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path      
# Create database if it doesn't exist
def create_database(app):
    db_path = os.path.join(app.root_path, 'sqlite_db', DB_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()


# Cookies and keys config   
def keys_cookies_config(app):
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    
              
#smtp
def smtp_config(app):
    if GMAIL and PASSWORD:
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USERNAME'] = GMAIL
        app.config['MAIL_PASSWORD'] = PASSWORD
    else:
        print("⚠️  MAIL_username or MAIL_password is not set. Email features will be disabled.")
 
    
# Login manager configuration
def login_manager_config():
    login_manager.login_view = '/'
    from website.models.database_models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

# Update user online status before each request
def last_seen_config(app):
    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated and current_user.role in ['user_role', 'other_user_role']:
            now = datetime.now(manila_tz).replace(second=0, microsecond=0)
            last_seen = current_user.last_seen
            if last_seen:
                last_seen = last_seen.astimezone(manila_tz).replace(second=0, microsecond=0)
            if not last_seen or (now - last_seen > timedelta(minutes=1)):
                current_user.last_seen = now
                db.session.commit()


