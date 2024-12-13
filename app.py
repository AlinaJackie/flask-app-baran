from flask import Flask
from students import students as students_blueprint
from extensions import db
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'your_secret_key'

# Ініціалізація LoginManager для Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'students.login'

# Ініціалізація Flask-Migrate
migrate = Migrate(app, db)

# Завантаження користувача (для Flask-Login)
from students.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Реєстрація Blueprint
app.register_blueprint(students_blueprint, url_prefix='/students')

# Ініціалізація бази даних
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

