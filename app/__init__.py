from flask import Flask
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
