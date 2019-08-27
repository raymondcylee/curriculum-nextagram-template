import re
from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from app import login_manager
from flask_login import login_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')



@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    
    input_username = request.form.get('username')
    input_password = request.form.get('password') 
    user = User.get_or_none(User.username == input_username) # None or a user
    
    if user:
        hashed_password = user.password
        result = check_password_hash(hashed_password, input_password)
        if result is True:
            login_user(user)
            return render_template('home.html')
        else:
            flash ('Wrong password')
            return redirect(url_for('sessions.new'))
    else:
        flash('One of the field is not right')
        return redirect(url_for('sessions.new'))
