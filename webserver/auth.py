import re
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from database import db, User
from utils import validate_json, logger
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from markupsafe import escape
from utils import logger

login_manager = LoginManager()
bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__)

pass_regex = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=_-])[A-Za-z0-9@#$%^&+=_-]{8,40}$')
user_regex = re.compile(r'^(?!.*[<>\'"\/\\{}\(\)\[\]\*\?\!\:\;\,\.\`|]).{3,12}$')

@auth_bp.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        if request.form.get('formType') == 'register':
            if User.query.filter_by(username=request.form.get('username')).first():
                flash('Username already exists.', category='error')
            elif not user_regex.match(request.form.get('username')):
                flash('Username must be 3–12 characters long and must not contain certain special characters.', category='error')
            elif not pass_regex.match(request.form.get('password')):
                flash('Password must contain at least one digit, one lowercase, one uppercase, one special character, and be 8–40 characters long.', category='error')
            else:
                try:
                    new_user = User(username=request.form.get('username'), password_hash=bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8'))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    # flash('Account successfully created!', category='success')
                    return redirect(url_for('auth.dashboard', m=2))
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"User creation failed: {e}")
                    flash('Account could not be created.', category='error')
        elif request.form.get('formType') == 'login':
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and bcrypt.check_password_hash(user.password_hash, request.form.get('password')):
                login_user(user)
                # flash('Logged in successfully!', category='success')
                return redirect(url_for('auth.dashboard', m=1))
            else:
                flash('Wrong credentials.', category='error')
    return render_template('auth/sign.html')

"""
Flask‑Login handles authentication through a session cookie containing the user’s user_id signed by your SECRET_KEY automatically loaded into current_user on every request, so we do not need tokens here, what it does for example:
session['_user_id'] = str(user.id) =>
session = {
    "_user_id": "42",
    "csrf_token": "abc123"
}
cookie = SIGNED(session, SECRET_KEY)
"""

@auth_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	m = request.args.get('m', default=None, type=int)
	if m==2:
		flash('Account successfully created!', category='success')
	elif m==1:
		flash('Logged in successfully!', category='success')
	return render_template('auth/dashboard.html')

@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logged out successfully!', category='success')
	return redirect(url_for('auth.sign'))

