from flask import Blueprint, render_template, session, flash, redirect, url_for
from models import Universe,Character

# Blueprint for world-related routes
worlds_bp = Blueprint('worlds', __name__)

# Route to display all universes
@worlds_bp.route('/worlds')
def show_worlds():
    if 'user_id' not in session:
        flash('Please log in.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    universes = Universe.query.all()

    character_counts = {}
    for universe in universes:
        count = Character.query.filter_by(universe_id=universe.id, user_id=user_id).count()
        character_counts[universe.id] = count

    return render_template('worlds.html', universes=universes, character_counts=character_counts)


# Route to view details of a single universe
@worlds_bp.route('/worlds/<int:universe_id>')
def view_world(universe_id):
    if 'user_id' not in session:
        flash('Please log in to view characters.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    universe = Universe.query.get_or_404(universe_id)

    characters = Character.query.filter_by(universe_id=universe.id, user_id=user_id).all()

    return render_template('view_world.html', universe=universe, characters=characters)

