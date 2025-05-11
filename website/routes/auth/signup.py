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

#-----------------
from website.config.security import (
    check_csrf,
    hash_password,
    check_email_format,
    check_password_strength,
    check_id_format
    )

#for smtp
'''
from website.config.smtp_mailer import(
    get_serializer,
    send_verification_email
)
'''

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

        check_csrf()
        data = request.get_json()
        first_name=data.get('first_name')
        last_name = data.get('last_name')
        user_id = data.get('user_id')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        #check all fields if empty
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
        #check password length
        if not (6 <= len(password) <= 20):
                return jsonify({'success': False, 'message': 'Password must be 6-20 characters'})
            
        invalid_email=check_email_format(email)
        invalid_password=check_password_strength(password)
        invalid_id=check_id_format(user_id)
        if invalid_email:return invalid_email
        if invalid_password:return invalid_password
        if invalid_id: return invalid_id
        
        
        # Check if user name already exists
        existing_user_name = User.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            ).first()
        if existing_user_name:
            return jsonify({'success': False, 'message': 'User already exist'})
        #check if ID is already used
        existing_id = User.query.filter_by(
            user_ID=user_id,
            ).first()
        if existing_id:
            return jsonify({'success': False, 'message': 'User ID already used'})
        #check if email already used
        existing_email= User.query.filter_by(
            email=email
            ).first()
        if existing_email:
            return jsonify({'success': False, 'message': 'Email already used'})
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            user_ID=user_id,
            email=email,
            password=hash_password(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        
        #for smtp email verification if needed
        '''
        # Generate verification token
        serializer = get_serializer()
        token = serializer.dumps(email, salt='email-confirm')
        confirm_url = url_for('verify_email.confirm_email', token=token, _external=True)
        # Send verification email
        send_verification_email(email, confirm_url)
        '''
        
        return jsonify({
            'success': True,
            'message': 'SignUp Successfully',
            'redirect': url_for('login.login_page')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
    
    

    
    

