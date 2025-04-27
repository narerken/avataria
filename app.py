from flask import Flask, render_template, redirect, url_for, flash, request, session, send_from_directory
from werkzeug.utils import secure_filename
from datetime import timedelta
import os

from config import Config
from models import db, User, Universe, Character
from forms import LoginForm, RegisterForm, CharacterForm
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)  # авто-выход через 5 минут


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.', 'warning')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in.', 'warning')
        return redirect(url_for('login'))
    characters = Character.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', characters=characters)


@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = CharacterForm()
    form.universe.choices = [(u.id, u.name) for u in Universe.query.all()]

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_character = Character(
            name=form.name.data,
            age=form.age.data,
            appearance=form.appearance.data,
            personality=form.personality.data,
            backstory=form.backstory.data,
            image_filename=filename,
            universe_id=form.universe.data,
            user_id=session['user_id']
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_character.html', form=form)


@app.route('/edit_character/<int:char_id>', methods=['GET', 'POST'])
def edit_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    form = CharacterForm(obj=character)
    form.universe.choices = [(u.id, u.name) for u in Universe.query.all()]

    if form.validate_on_submit():
        character.name = form.name.data
        character.age = form.age.data
        character.appearance = form.appearance.data
        character.personality = form.personality.data
        character.backstory = form.backstory.data
        character.universe_id = form.universe.data

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            character.image_filename = filename

        db.session.commit()
        flash('Character updated!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_character.html', form=form)


@app.route('/delete_character/<int:char_id>', methods=['POST'])
def delete_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(character)
    db.session.commit()
    flash('Character deleted!', 'info')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
