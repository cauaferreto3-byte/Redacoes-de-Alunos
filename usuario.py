#[ ] Autenticação: Rotas /auth/register e /auth/login (JWT).
#• [ ] Rota de Perfil: PUT /profile para o aluno atualizar sua meta ou foto de 
#perfil.

from flask import Flask, Blueprint, request
from sqlalchemy import text
from database import db



usuario_bp = Blueprint('usuario', __name__, url_prefix = '/usuario') 

#Conexao Geral do meu app
#db = SQLAlchemy(app) #conecta

@usuario_bp.route("/auth/register", methods=["POST"])
def cadastro():
    #dados que vieram
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    curso_alvo = request.form.get("curso_alvo")
    universidade = request.form.get("universidade")
    foto = request.form.get("foto")

    if not email or email.endswith("@admin.com"):
        return {"erro": "Informe um email de usuario!"}, 400

    # Proíbe letras maiúsculas na parte local (antes do @)
    local = email.split('@', 1)[0]
    if any(ch.isupper() for ch in local):
        return {"erro": "O email não pode conter letras maiúsculas antes do @."}, 400
    
    if not nome or not nome.strip():
        return {"erro": "nome nao encontrado."}, 400
    elif not senha or not senha.strip():
        return {"erro": "senha nao encontrada."}, 400
    elif not curso_alvo or not curso_alvo.strip():
        return {"erro": "Infome seu objetivo de curso."}, 400
    elif not universidade or universidade.strip():
        return {"erro": "Universidade nao encontrada."}, 400
    elif not foto or not foto.strip():
        return {"erro": "URL da foto nao encontrada."}, 400

    #SQL
    sql = text("INSERT INTO usuario (nome, senha, email, curso_alvo, universidade, foto) VALUES (:nome, :senha, :email, :curso_alvo, :universidade, :foto) RETURNING id")
    dados = {"nome": nome, "senha": senha, "email": email, "curso_alvo": curso_alvo, "universidade": universidade, "foto": foto} #os dados do que veio lá da var sql

    #executar consulta
    result = db.session.execute(sql, dados)
    db.session.commit()#commit é "lento"

    #pega o id
    id = result.fetchone()[0] #lá do RETURNING id
    dados['id'] = id


    return dados


@usuario_bp.route("/auth/login", methods=["POST"])
def login():
    email = request.form.get("email"),
    senha = request.form.get("senha")

    sql = text("SELECT * FROM usuario WHERE senha = :senha AND email = :email")
    dados = {"senha": senha, "email": email}
   
    result = db.session.execute(sql, dados)

    if result.rowcount == 1:
      return "Usuário Logado!"
    else:
        return "Senha ou email incorreto. Tente novamente!"  

@usuario_bp.route("/profile/<id>", methods=["PUT"])
def atualizar_foto(id):
    foto = request.form.get("foto")

    if not foto or not foto.strip():
        return {"erro": "URL da foto nao encontrada ou corrompida."}, 400
    
    sql = text("UPDATE usuario SET foto = :foto WHERE id = :id")
    dados = {"foto": foto, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Foto com o {id} atualizada"
    else:
        db.session.rollback()
        return f"problemas ao atualizar dados"



