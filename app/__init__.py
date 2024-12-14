from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Змінив FlaskBcrypt на Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)  # Використовуємо Bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes, models

