from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, Character, Universe
from forms import CharacterForm
import os
from werkzeug.utils import secure_filename
from config import Config

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in.', 'warning')
        return redirect(url_for('auth.login'))
    characters = Character.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', characters=characters)

@characters_bp.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    form = CharacterForm()
    form.universe.choices = [(u.id, u.name) for u in Universe.query.all()]

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(Config.UPLOAD_FOLDER, filename))

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
        return redirect(url_for('characters.dashboard'))

    return render_template('create_character.html', form=form)

@characters_bp.route('/edit_character/<int:char_id>', methods=['GET', 'POST'])
def edit_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('characters.dashboard'))

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
            form.image.data.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            character.image_filename = filename

        db.session.commit()
        flash('Character updated!', 'success')
        return redirect(url_for('characters.dashboard'))

    return render_template('edit_character.html', form=form)

@characters_bp.route('/delete_character/<int:char_id>', methods=['POST'])
def delete_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('characters.dashboard'))
    db.session.delete(character)
    db.session.commit()
    flash('Character deleted!', 'info')
    return redirect(url_for('characters.dashboard'))
