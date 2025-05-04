from flask import Flask, render_template, session
from config import Config
from models import db
from datetime import timedelta

# Import Blueprints
from auth.routes import auth_bp
from characters.routes import characters_bp
from worlds.routes import worlds_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(characters_bp)
app.register_blueprint(worlds_bp)

# Make user session permanent and set expiration time
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
