import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env para o ambiente do sistema
load_dotenv()

db = SQLAlchemy()

def init_db(app):
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost/redacao'

    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        raise ValueError("A variável de ambiente DATABASE_URL não foi definida")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)