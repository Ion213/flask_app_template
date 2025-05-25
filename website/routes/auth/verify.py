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
from website.config.smtp_mailer import send_verification_email,get_serializer
from website.config.security import check_csrf,check_email_format

from website.config.modules import db
from website.models.database_models import User

manila_tz = timezone('Asia/Manila')

#create blueprint/routes
verify = Blueprint('verify', __name__)

#render the verification page
@verify.route('/verify_email_page/<token>', methods=['GET'])
def verify_email_page(token):
    try:
        serializer = get_serializer()
        # Validate the token with a  expiration
        email = serializer.loads(token, salt='email-confirm', max_age=180)

        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("auth/verify.jinja2", message="Invalid or expired token", success=False)

        if user.is_verified:
            return render_template("auth/verify.jinja2", message="This email has already been verified.", success=True)

        # Mark user as verified
        user.is_verified = True
        db.session.commit()

        return render_template("auth/verify.jinja2", message="Your email has been verified successfully!", success=True)

    except SignatureExpired:
        return render_template("auth/verify.jinja2", message="The confirmation link has expired. Please request a new one.", success=False)

    except BadSignature:
        return render_template("auth/verify.jinja2", message="Invalid confirmation link.", success=False)
    
    
#verify resend link
@verify.route('/resend_link', methods=['POST'])
def resend_link():
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

        if user.is_verified:
            return jsonify({'success': True, 'message': 'This email is already verified.'})

        # Generate a new verification token
        serializer = get_serializer()
        token = serializer.dumps(email, salt='email-confirm')
        link = url_for('verify.verify_email_page', token=token, _external=True)
        # Send the verification email
        send_verification_email(email, link)
        
        return jsonify({'success': True, 'message': 'A new verification link has been sent. Check your email inbox or spam.'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})