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


from itsdangerous import SignatureExpired, BadSignature
from website.config.smtp_mailer import send_reset_password_link,get_serializer

from website.config.security import (
    check_csrf,
    check_email_format,
    hash_password,
    check_password_strength
    )

from website.config.modules import db
from website.models.database_models import User

manila_tz = timezone('Asia/Manila')

forgot_pass = Blueprint('forgot_pass', __name__)

# render forgot pass page
@forgot_pass.route('/forgot_pass_page', methods=['GET'])
def forgot_pass_page():
    return render_template('auth/forgot_pass.jinja2')

#send reset password link
@forgot_pass.route('/send_reset_link', methods=['POST'])
def send_reset_link():
    try:
        check_csrf()
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email is required.'})
        
        invalid_email=check_email_format(email)
        if invalid_email: return invalid_email

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found.'})
        
        if not user.is_verified:
            return jsonify({'success': False, 'message': 'This email is not verified. Please verify it first'})

        # Generate a reset token
        serializer = get_serializer()
        token = serializer.dumps(email, salt='password-reset')
        link = url_for('forgot_pass.change_pass_page', token=token, _external=True)
        # Send the reset link email
        send_reset_password_link(email, link)
        
        return jsonify({'success': True, 'message': 'Password reset link sent. Check your email inbox or spam.'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
    
#render change pass page
@forgot_pass.route('/change_pass_page/<token>', methods=['GET','POST'])
def change_pass_page(token):
    serializer = get_serializer()
    #GET/render the page
    if request.method == 'GET':
        try:
            # Validate the token with a  expiration
            email = serializer.loads(token, salt='password-reset', max_age=180)

            user = User.query.filter_by(email=email).first()
            if not user:
                return render_template("auth/change_pass.jinja2", message="Invalid or expired token", success=False,token=token)

            if not user.is_verified:
                return render_template("auth/change_pass.jinja2", message="This email is not verified. Please verify it first", success=False,token=token)


            return render_template("auth/change_pass.jinja2", message="Input a new password.", success=True,token=token)

        except SignatureExpired:
            return render_template("auth/change_pass.jinja2", message="The reset link has expired. Please request a new one.", success=False,token=token)

        except BadSignature:
            return render_template("auth/change_pass.jinja2", message="Invalid reset password link.", success=False,token=token)
        
    #POST/Change password submit
    if request.method == 'POST':
        try:
            check_csrf()
            data = request.get_json()
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            email = serializer.loads(token, salt='password-reset', max_age=180)
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'success': False, 'message': 'Invalid or expired token'})
            if not user.is_verified:
                return jsonify({'success': False, 'message': 'This email is not verified. Please verify it first.'})

            if not password or not confirm_password:
                return jsonify({'success': False, 'message': 'All fields are required'})

            if password != confirm_password:
                return jsonify({'success': False, 'message': 'Passwords do not match'})
            #check password length
            if not (6 <= len(password) <= 20):
                    return jsonify({'success': False, 'message': 'Password must be 6-20 characters'})
            
            invalid_password=check_password_strength(password)
            if invalid_password: return invalid_password

            user.password = hash_password(password)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Password changed successfully.'})

        except SignatureExpired:
            return jsonify({'success': False, 'message': 'The reset link has expired. Please request a new one.'})
        except BadSignature:
            return jsonify({'success': False, 'message': 'Invalid reset password link.'})
    
    