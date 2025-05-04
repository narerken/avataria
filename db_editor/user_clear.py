import os
import sys

# Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import app  # импортируй свое приложение
from models import db, User  # импортируй модели

# Очищаем таблицу пользователей внутри контекста приложения
with app.app_context():
    deleted_count = User.query.delete()
    db.session.commit()
    print(f"Deleted {deleted_count} users.")
