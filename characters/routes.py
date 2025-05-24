from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, Character, Universe
from forms import CharacterForm
import os
from werkzeug.utils import secure_filename
from config import Config

# Blueprint for character-related routes
characters_bp = Blueprint('characters', __name__)

# Dashboard view showing user's characters
@characters_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in.', 'warning')
        return redirect(url_for('auth.login'))

    # Get all characters belonging to the logged-in user
    characters = Character.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', characters=characters)

# Create a new character
@characters_bp.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    form = CharacterForm()

    # Подставим AI-данные, если есть
    ai_data = session.pop('ai_character', None)
    if ai_data:
        form.name.data = ai_data.get('name')
        form.age.data = ai_data.get('age')
        form.appearance.data = ai_data.get('appearance')
        form.personality.data = ai_data.get('personality')
        form.backstory.data = ai_data.get('backstory')

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

# Edit an existing character
@characters_bp.route('/edit_character/<int:char_id>', methods=['GET', 'POST'])
def edit_character(char_id):
    character = Character.query.get_or_404(char_id)

    # Ensure the character belongs to the current user
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('characters.dashboard'))

    form = CharacterForm(obj=character)
    form.universe.choices = [(u.id, u.name) for u in Universe.query.all()]

    if form.validate_on_submit():
        # Update character fields
        character.name = form.name.data
        character.age = form.age.data
        character.appearance = form.appearance.data
        character.personality = form.personality.data
        character.backstory = form.backstory.data
        character.universe_id = form.universe.data

        # Handle new image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            character.image_filename = filename

        db.session.commit()
        flash('Character updated!', 'success')
        return redirect(url_for('characters.dashboard'))

    return render_template('edit_character.html', form=form)

# Delete a character
@characters_bp.route('/delete_character/<int:char_id>', methods=['POST'])
def delete_character(char_id):
    character = Character.query.get_or_404(char_id)

    # Check ownership before deleting
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('characters.dashboard'))

    db.session.delete(character)
    db.session.commit()
    flash('Character deleted!', 'info')
    return redirect(url_for('characters.dashboard'))


# View character details
@characters_bp.route('/character/<int:char_id>')
def view_character(char_id):
    character = Character.query.get_or_404(char_id)

    # Только владелец может просматривать персонажа (можно убрать, если доступ публичный)
    if character.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('characters.dashboard'))

    return render_template('view_character.html', character=character)
