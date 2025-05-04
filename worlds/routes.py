from flask import Blueprint, render_template
from models import Universe

# Blueprint for world-related routes
worlds_bp = Blueprint('worlds', __name__)

# Route to display all universes
@worlds_bp.route('/worlds')
def show_worlds():
    universes = Universe.query.all()
    return render_template('worlds.html', universes=universes)

# Route to view details of a single universe
@worlds_bp.route('/worlds/<int:universe_id>')
def view_world(universe_id):
    universe = Universe.query.get_or_404(universe_id)
    return render_template('view_world.html', universe=universe)
