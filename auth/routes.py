from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db, User
from forms import LoginForm, RegisterForm

# Auth blueprint
auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('characters.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('characters.dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html', form=form)

# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('The passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('A user with that name already exists.', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration was successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# Logout route
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))
