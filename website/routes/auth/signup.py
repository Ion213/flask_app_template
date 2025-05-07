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


manila_tz = timezone('Asia/Manila')

signup = Blueprint('signup', __name__)

# render schedule template
@signup.route('/signup_page', methods=['GET'])
def signup_page():
    return render_template('public/signup.jinja2')
