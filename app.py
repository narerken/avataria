from flask import Flask, render_template, session
from config import Config
from models import db
from datetime import timedelta

# Импортируем Blueprints
from auth.routes import auth_bp
from characters.routes import characters_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Регистрируем Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(characters_bp)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
