from flask import Flask
<<<<<<< HEAD
from app.routes import main_bp
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
    app.register_blueprint(main_bp)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
=======
from .routes import main_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates')
    app.register_blueprint(main_bp)
    return app
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
