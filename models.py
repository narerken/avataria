from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User model with password hashing
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    characters = db.relationship('Character', backref='owner', lazy=True)

    # Hash and store password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Universe model to group characters
class Universe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    alignment = db.Column(db.String(10), nullable=False, default="neutral")  # e.g., good, evil, neutral
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)  # Optional image
    characters = db.relationship('Character', backref='universe', lazy=True)

# Character model linked to both Universe and User
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    appearance = db.Column(db.Text, nullable=False)
    personality = db.Column(db.Text, nullable=False)
    backstory = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(300))  # Path to uploaded image
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
