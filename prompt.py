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



