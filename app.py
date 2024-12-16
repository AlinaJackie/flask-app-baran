from flask import Flask
from posts import posts_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Реєстрація блюпринта
app.register_blueprint(posts_bp, url_prefix='/posts')

if __name__ == '__main__':
    app.run(debug=True)


