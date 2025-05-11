from flask import request,jsonify,redirect, url_for
from functools import wraps
from flask_login import current_user

from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import re


#csrf token checker --for every routes more secure every request
def check_csrf():
    csrf_token = request.headers.get('X-CSRFToken') or request.form.get('csrf_token')
    if not csrf_token:
        raise ValidationError("Missing CSRF token.")
    validate_csrf(csrf_token)

#password hash generator  -->  for signup
def hash_password(password):
    return generate_password_hash(password)

#validate password hash match to password --> for login
def verify_password(hashed, password):
    return check_password_hash(hashed, password)

#email check format
def check_email_format(email):    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'success': False, 'message': 'Invalid email format.'})
#check password strength
def check_password_strength(password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,20}$'
    if not re.match(password_pattern, password):
        return jsonify({'success': False, 'message': 'Password must be 6–20 chars, includes: A-Z, a-z, 0-9, and symbol (e.g. @, #, $).✘'})
#check id format
def check_id_format(user_ID):
    id_pattern = r'^\d+(?:-\d+)+$'
    if not re.match(id_pattern, user_ID):
        return jsonify({'success': False, 'message': 'Invalid Student ID format. It should be numbers separated by hyphens (e.g., 2017-21-00062).'})
        
    
#-----------------check if the user is allowed in particular routes
def role_required_multiple(*required_roles):  # Accepts multiple roles as arguments
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in required_roles:  # Check if role is allowed
                return redirect(url_for('login.login_page'))  # Redirect back to login page if role is not allowed
            return func(*args, **kwargs)
        return wrapper
    return decorator


#-----------------check if already login or not
def is_user_authenticated(role):
    if role in ['admin', 'staff']:
        return redirect(
            url_for('user.user_page')#change this to the admin/staff main page or dashboard if implemented
            )
    elif role == 'client':
        return redirect(
            url_for('user.user_page') #change this to the client main page or dashboard if implemented
            )
    return redirect(url_for('login.login_page')) #if not login it back to default-login page you can change this if you want