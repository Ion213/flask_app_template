from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from website.config.modules import mail
from website.config.env_loader import (
    GMAIL,
    SECRET_KEY
)

# send email verification link
def send_verification_email(email, confirm_url):
    msg = Message('Confirm Your Email', sender=GMAIL, recipients=[email])
    msg.body = (
        f"Hello,\n\n"
        f"Please confirm your email address by clicking the link below:\n"
        f"{confirm_url}\n\n"
        f"This link will expire in 3 minutes. If you didn’t request this, please ignore it."
        f"Do not share this link with anyone."
    )
    mail.send(msg)
    
# Send reset password link
def send_reset_password_link(email,reset_url):
    msg = Message('Password Reset Request', sender=GMAIL, recipients=[email])
    msg.body = f'Click the link to reset your password: {reset_url}'
    mail.send(msg)

# Secure serializer (initialize in flask_app)
def get_serializer():
    return URLSafeTimedSerializer(f'{SECRET_KEY}')  # Use actual secret key