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

login = Blueprint('login', __name__)

# render schedule template
@login.route('/login_page', methods=['GET'])
def login_page():
    return render_template('auth/login.jinja2')
