<<<<<<< HEAD
import os
from dotenv import load_dotenv
from flask import Flask
from app.routes import main_bp

# Carrega variáveis de ambiente do .env
load_dotenv()

def create_app():
    """
    Cria e configura a instância do Flask:
    - Aponta para app/static e app/templates
    - Registra o blueprint com todas as rotas
    """
    app = Flask(
        __name__,
        static_folder="app/static",
        template_folder="app/templates"
    )
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
    app.register_blueprint(main_bp)
    return app

# Instância global necessária para o `flask run`
app = create_app()

if __name__ == "__main__":
    # Também funciona chamando diretamente o arquivo
    app.run(debug=True)
=======
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
