from app import app, db
from models import Universe

def seed_universes():
    universes = ['Fantasy World', 'Sci-Fi Galaxy', 'Historical Era']
    for name in universes:
        existing = Universe.query.filter_by(name=name).first()
        if not existing:
            new_universe = Universe(name=name)
            db.session.add(new_universe)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_universes()
