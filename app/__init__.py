from flask import Flask
import os


def create_app():
    app = Flask(__name__,
                template_folder=os.path.abspath("app/templates"),
                static_folder=os.path.abspath("app/static"))

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app