from flask import Flask, Blueprint, request
from sqlalchemy import text
from database import db



redacoes_bp = Blueprint('redacoes', __name__, url_prefix = '/redacoes') 

@redacoes_bp.route('/create', methods=['POST'])
def criarRedacao():
    titulo = request.form.get("titulo")
    tema = request.form.get("tema")
    texto = request.form.get("texto")
    status = request.form.get("status")
    id_aluno = request.form.get("id_aluno")

    # Validação: texto deve ter no mínimo 50 caracteres
    if not texto or len(texto) < 50:
        return {"erro": "O texto deve ter no mínimo 50 caracteres"}, 400

    sql = text("INSERT INTO redacoes(titulo, tema, texto, status, id_aluno) VALUES (:titulo, :tema, :texto, :status, :id_aluno)")
    dados = {"titulo": titulo, "tema": tema, "texto": texto, "status": status, "id_aluno": id_aluno}

    db.session.execute(sql, dados)
    db.session.commit()

    return dados

@redacoes_bp.route('/getOne/<id>')
def getOne(id):

    sql = text("SELECT * FROM redacoes WHERE id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e

@redacoes_bp.route('/update/<id>', methods=["PUT"])
def update(id):
    titulo = request.form.get("titulo")
    tema = request.form.get("tema")
    texto = request.form.get("texto")
    status = request.form.get("status")

    # Validação: proibir renomear ou permanecer status como "Pendente"
    if status == "Pendente":
        return {"erro": "Nao pode ser pendente enquanto houver atualizacao na redacao"}, 400

    sql = text("UPDATE redacoes SET titulo = :titulo, tema = :tema, texto = :texto, status = :status WHERE id = :id") 
    dados = {"titulo": titulo, "tema": tema, "texto": texto, "status": status, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Redação com o id:{id} atualizado!"
    else:
        db.session.rollback()
        return f"problemas ao atualizar dados"

@redacoes_bp.route('/delete/<id>', methods=["DELETE"])
def delete(id):
    sql = text("DELETE FROM redacoes WHERE id = :id")
    dados = {"id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Redação com o id:{id} removida"
    else:
        db.session.rollback()
        return f"Só deus na causa"

@redacoes_bp.route('/aluno/<id_aluno>')
def redacoes_por_aluno(id_aluno):
    sql = text("SELECT * FROM redacoes WHERE id_aluno = :id_aluno")
    dados = {"id_aluno": id_aluno}

    try:
        result = db.session.execute(sql, dados)
        linhas = result.mappings().all()
        
        if not linhas:
            return {"mensagem": "Nenhuma redação encontrada para este aluno"}, 404
        
        return [dict(linha) for linha in linhas], 200
    except Exception as e:
        return {"erro": str(e)}, 500