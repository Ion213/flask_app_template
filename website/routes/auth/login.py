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


from website.models.database_models import User

manila_tz = timezone('Asia/Manila')

login = Blueprint('login', __name__)

# render schedule template
@login.route('/login_page', methods=['GET'])
def login_page():
    return render_template('auth/login.jinja2')

#login submit
@login.route('/login_submit', methods=['POST'])
def login_submit():
    try:
        csrf_token = request.headers.get('X-CSRFToken')
        validate_csrf(csrf_token)
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email:
            return jsonify({'success': False, 'message': 'Please provide email'})
        if not password:
            return jsonify({'success': False, 'message': 'Please provide password'})

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'})

        if not check_password_hash(user.password, password):
            return jsonify({'success': False, 'message': 'Invalid email or password'})

        # You can use login_user(user) here if using Flask-Login
        return jsonify({'success': True, 'message': 'Login successful'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


