from flask import Blueprint, request
from sqlalchemy import text
from database import db

adm_bp = Blueprint('adm', __name__, url_prefix = '/adm')

@adm_bp.route('/create', methods=['POST'])
def criar_adm():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    id_aluno = request.form.get("id_aluno")

    sql = text("INSERT INTO adm (nome, email, senha, id_aluno) VALUES (:nome, :email, senha:, :id_aluno)")
    dados = {"nome": nome, "email": email, "senha": senha, "id_aluno": id_aluno}

    db.session.execute(sql, dados)

    if email.endswith() == '@admin.com':
        db.session.commit()
        return dados
        #return "Conta criada!"
    else:
        db.session.rollback()
        return "Email inválido para um admin."
    