from flask_login import UserMixin
from datetime import datetime,time


from website.config.modules import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True) 
    date_registered = db.Column(db.DateTime, nullable=True)
    date_updated = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(50), nullable=False, default='client')
    is_verified = db.Column(db.Boolean, default=False)
    is_deactivated=db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime,nullable=True)
    
    logs = db.relationship('Logs', backref='user', lazy=True, cascade="all, delete-orphan")

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_info= db.Column(db.String(100), nullable=True)
    activity_time = db.Column(db.DateTime,nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
