from flask import Blueprint, request
from sqlalchemy import text
from database import db

adm_bp = Blueprint('adm', __name__, url_prefix = '/adm')

@adm_bp.route('/create', methods=['POST'])
def criar_adm():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    log_atividade = request.form.get("log_atividade")

    if not nome or not nome.strip():
        return {"erro": "Informe seu nome."}, 400
    elif not senha or not senha.strip():
        return {"erro": "Senha nula, digite-a."}, 400
    
    # Valida email: domínio e ausência de maiúsculas na parte local
    if not email or not email.endswith("@admin.com"):
        return "Email inválido para um admin."

    local = email.split('@', 1)[0]
    if any(ch.isupper() for ch in local):
        return {"erro": "O email não pode conter letras maiúsculas antes do @."}, 400

    sql = text("INSERT INTO adm (nome, email, senha, log_atividade) VALUES (:nome, :email, :senha, :log_atividade)")
    dados = {"nome": nome, "email": email, "senha": senha, "log_atividade": log_atividade}
    db.session.execute(sql, dados)
    db.session.commit()

    return dados
    

@adm_bp.route('/getOne/<id>')
def get_one_adm(id):

    sql = text("SELECT * FROM adm WHERE id = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e


@adm_bp.route('/getAll')
def get_all_adm():
    sql_query = text("SELECT * FROM adm") #LIMIT 100 OFFSET 100 para paginação
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambi pq cada linha é um objeto

        print(json)

        return json
    except Exception as e:
        return e

@adm_bp.route('/update/<id>', methods=["PUT"])
def updateADM(id):
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    log_atividade = request.form.get("log_atividade")

    # Verifica se o administrador com o id existe
    exists_sql = text("SELECT 1 FROM adm WHERE id = :id")
    exists = db.session.execute(exists_sql, {"id": id}).first()
    if not exists:
        return {"erro": f"Administrador com id {id} não encontrado."}, 404

    if not email or not email.endswith("@admin.com"):
        return {"erro": "Informe um email legítimo de administrador!"}, 400

    # Proíbe letras maiúsculas na parte local (antes do @)
    local = email.split('@', 1)[0]
    if any(ch.isupper() for ch in local):
        return {"erro": "O email não pode conter letras maiúsculas antes do @."}, 400
    
    if not nome or not nome.strip():
        return {"erro": "Informe seu nome."}, 400
    elif not senha or not senha.strip():
        return {"erro": "Digite sua senha."}, 400

    sql = text("UPDATE adm SET nome = :nome, email = :email, senha = :senha, log_atividade = :log_atividade WHERE id = :id") 
    dados = {"nome": nome, "email": email, "senha": senha, "log_atividade": log_atividade, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
   
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Administrador com o id:{id} atualizado!"
    else:
        db.session.rollback()
        return f"problemas ao atualizar dados"
 
@adm_bp.route('/delete/<id>', methods=["DELETE"])
def delete_adm(id):
    sql = text("DELETE FROM adm WHERE id = :id")
    dados = {"id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Administrador com o id:{id} removida"
    else:
        db.session.rollback()
        return f"Só deus na causa"