#[ ] Autenticação: Rotas /auth/register e /auth/login (JWT).
#• [ ] Rota de Perfil: PUT /profile para o aluno atualizar sua meta ou foto de 
#perfil.


#email = input("Digite seu endereço de e-mail: ").strip().lower()

#def verificar_email(endereco):
#    return "@" in endereco and endereco.endswith(".com")

#if verificar_email(email):
 #   print("✅ E-mail válido!")
#else:
 #   print("❌ E-mail inválido. Certifique-se de incluir '@' e terminar com '.com'.")

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
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha")
    numero_curso = request.form.get("numero_curso")
    universidade = request.form.get("universidade")
    foto = request.form.get("foto")

    # Validação usando find(): localizar '@' (exatamente um) e garantir que tenha ao menos 4 caracteres após ele
    if not email:
        return {"erro": "Informe um email de usuário!"}, 400

    if ' ' in email:
        return {"erro": "Email não pode conter espaços."}, 400

    # verifica se há exatamente um '@'
    if email.count('@') != 1:
        return {"erro": "Informe um email com exatamente um '@'."}, 400

    local = email.split('@', 1)[1] #verificar que esse ponto esteja APÓS o @, não antes.
    
    # garante pelo menos 4 caracteres após o '@'
    if len(local) < 4:
        return {"erro": "A parte após o '@' deve ter ao menos 4 caracteres."}, 400
    
    if local.count('.') < 1:
         return {"erro": "Nenhuma informação com '.' após o '@'. Melhor checar!"}, 400

    if email.endswith("admin.com"):
        return "Informe um email de usuário! Conta administradora é inválida nesse setor."

    entensao = ('jpg', 'png', 'jpeg', 'webp')

    if not foto or not foto.strip():
        return {"erro": "URL da foto nao encontrada."}, 400
    if not foto.endswith(entensao):
        return {"erro": "URL de foto inválida, por favor verifique o formato da foto."}, 400
    
    if not nome or not nome.strip():
        return {"erro": "nome nao encontrado."}, 400
    elif not senha or not senha.strip():
        return {"erro": "senha nao encontrada."}, 400
    elif not numero_curso or not numero_curso.strip():
        return {"erro": "Infome seu objetivo de curso."}, 400
    elif not universidade or not universidade.strip():
        return {"erro": "Universidade nao encontrada."}, 400
    
    
    #SQL
    sql = text("INSERT INTO usuario (nome, senha, email, numero_curso, universidade, foto) VALUES (:nome, :senha, :email, :numero_curso, :universidade, :foto) RETURNING id")
    dados = {"nome": nome, "senha": senha, "email": email, "numero_curso": numero_curso, "universidade": universidade, "foto": foto} #os dados do que veio lá da var sql

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

    entensao = ('jpg', 'png', 'jpeg', 'webp')
    if not foto or not foto.strip():
        return {"erro": "URL da foto nao encontrada ou corrompida."}, 400
    if not foto.endswith(entensao):
        return {"erro": "URL de foto inválida, por favor verifique o formato da foto."}, 400

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



