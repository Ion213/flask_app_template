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


from website.config.security import (
    check_csrf,
    check_email_format,
    verify_password
)
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
        
        check_csrf()
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email:
            return jsonify({'success': False, 'message': 'Please provide email'})
        if not password:
            return jsonify({'success': False, 'message': 'Please provide password'})
        
        invalid_email=check_email_format(email)
        if invalid_email:return invalid_email
        
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'})

        if not verify_password(user.password, password):
            return jsonify({'success': False, 'message': 'Invalid email or password'})

        # more logic here if needed like role base conditions
        
        return jsonify({
            'success': True, 
            'message': 'Login successful',
            'redirect': url_for('login.login_page') #change this to the actual user page if you implemented
            }) 

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


