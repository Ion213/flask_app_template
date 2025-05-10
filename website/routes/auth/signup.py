#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash,
    jsonify
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )

from pytz import timezone
from datetime import datetime
from sqlalchemy import or_,and_,extract
from sqlalchemy.sql import func

from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash


from website.config.modules import db
from website.models.database_models import User

manila_tz = timezone('Asia/Manila')

signup = Blueprint('signup', __name__)

#signup html
@signup.route('/signup_page', methods=['GET'])
def signup_page():
    return render_template('auth/signup.jinja2')

#signup submit
@signup.route('/signup_submit', methods=['POST'])
def signup_submit():
    try:
        csrf_token = request.headers.get('X-CSRFToken')
        validate_csrf(csrf_token)
        
        data = request.get_json()
        first_name=data.get('first_name')
        last_name = data.get('last_name')
        user_id = data.get('user_id')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not first_name:
            return jsonify({'success': False, 'message':'Please provide first name'})
        if not last_name:
            return jsonify({'success': False, 'message':'Please provide flast name'})
        if not user_id:
            return jsonify({'success': False, 'message':'Please provide user ID'})
        if not email:
            return jsonify({'success': False, 'message':'Please provide email'})
        if not password:
            return jsonify({'success': False, 'message':'Please provide password'})
        if not confirm_password:
            return jsonify({'success': False, 'message':'Please provide confirm_password'})
        
        # Check if password and confirm password match
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'})
        
        # Check if user already exists
        existing_user_name = User.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            ).first()
        if existing_user_name:
            return jsonify({'success': False, 'message': 'User already exist'})
        
        existing_id = User.query.filter_by(
            user_ID=user_id,
            ).first()
        if existing_id:
            return jsonify({'success': False, 'message': 'User ID already used'})
        
        existing_email= User.query.filter_by(
            email=email
            ).first()
        if existing_email:
            return jsonify({'success': False, 'message': 'Email already used'})
        
        # Create the new user (hash password before storing)
        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            user_ID=user_id,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'SignUp Successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
    
    

    
    

