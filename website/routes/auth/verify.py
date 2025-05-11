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
from website.config.security import check_csrf

from website.config.modules import db
from website.models.database_models import User

manila_tz = timezone('Asia/Manila')

#create blueprint/routes
verify = Blueprint('verify', __name__)

@verify.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
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
    
    
#verify resend
@verify.route('/resend_link', methods=['POST'])
def resend_link():
    check_csrf()
    email = request.form.get('email')
    if not email:
        return render_template("auth/verify.jinja2", message="Email is required.", success=False)

    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template("auth/verify.jinja2", message="User not found.", success=False)

    if user.is_verified:
        return render_template("auth/verify.jinja2", message="This email is already verified.", success=True)

    # Generate a new verification token
    serializer = get_serializer()
    token = serializer.dumps(email, salt='email-confirm')
    link = url_for('verify.verify_email', token=token, _external=True)
    # Send the verification email
    send_verification_email(email, link)

    return render_template("auth/verify.jinja2", message="A new verification link has been sent. Check your email inbox or spam.", success=False)