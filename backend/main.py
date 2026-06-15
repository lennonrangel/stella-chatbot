from flask import Flask 
from flask_cors import CORS
from backend.api.routes import bp
from backend.db.database import init_db
from dotenv import load_dotenv  
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    CORS(app)
    app.register_blueprint(bp)

    with app.app_context():
        init_db()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
