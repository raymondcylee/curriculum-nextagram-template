import re
from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from models.user import User
from app import login_manager, S3_BUCKET, s3
from flask_login import logout_user, login_required, current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    errors = []
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    repeatpassword = request.form.get("repeatpassword")

    if password != repeatpassword:
        # flash('Invalid password')
        errors.append("Invalid password")
        return render_template('users/new.html', username=request.form.get('username'),email=request.form.get('email'), errors=errors)


    newuser = User(name=name, username=username, email=email, password=password)
    if newuser.save():
        flash('User created')
        return render_template('sessions/new.html')
    else:
        errors += newuser.errors
    return render_template('users/new.html', username=request.form.get('username'),email=request.form.get('email'), errors=errors)

@users_blueprint.route('/signin', methods=["GET"])
def sign_in():
    return render_template('users/sign_in.html')

@users_blueprint.route('/logout', methods=["POST"])
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))

@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('users/username.html')
    else:
        return abort(404)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('users/edit.html')


@users_blueprint.route('/update', methods=['POST'])
def update():
    errors = []
    input_name = request.form.get('newname')
    input_username = request.form.get('new_username')
    user = User.get_or_none(User.id == current_user.id)

    if input_name:
        user.name = input_name
    if input_username:
        user.username = input_username

    if user.save():
        flash('Info updated')
        return redirect(url_for('users.edit'))
    else:
        errors += user.errors
    return render_template('users/edit.html', errors=errors)

@users_blueprint.route('/upload', methods=["POST"])
def upload( acl="public-read"):

        s3.upload_fileobj(
            request.files.get('user_file'),
            S3_BUCKET,
            request.files.get('user_file').filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": request.files.get('user_file').content_type
            }
        )

