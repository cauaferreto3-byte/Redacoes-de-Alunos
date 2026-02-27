from flask import Blueprint, request
from sqlalchemy import text
from database import db



avaliacao_bp = Blueprint('avaliacao', __name__, url_prefix = '/avaliacao') 

@avaliacao_bp.route('/create', methods=['POST'])
def inserirAvaliacao():
    nota_final = request.form.get("nota_final")
    id_redacao = request.form.get("id_redacao")
    comentario = request.form.get("comentario")
    data_avaliacao = request.form.get("data_avaliacao")
    id_adm = request.form.get("id_adm")

    if not nota_final or not nota_final.strip():
        return "Nota nao encontrada."
    if not comentario or not comentario.strip():
        return "Comentario inexistente"
    if not data_avaliacao or not data_avaliacao.strip():
        return "Falha ao procurar a data da avaliacao"
    if not id_redacao or not id_redacao.strip():
        return "Falha ao tentar identificar a redacao."
    if not id_adm or not id_adm.strip():
       return "Avaliador nao identificado." 

    sql = text("INSERT INTO avaliacao(nota_final, id_redacao, comentario, data_avaliacao, id_adm) VALUES (:nota_final, :id_redacao, :comentario, :data_avaliacao, :id_adm)")
    dados = { "nota_final": nota_final, 
        "id_redacao": id_redacao, 
         "comentario": comentario, "data_avaliacao": data_avaliacao,
         "id_adm": id_adm
         }

    db.session.execute(sql, dados)
    db.session.commit()

    return dados

@avaliacao_bp.route('/getOne/<id>')
def getOne_avaliacao(id):

    sql = text("SELECT * FROM avaliacao WHERE id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e


@avaliacao_bp.route('/getAll')
def get_all_avaliacao():
    sql_query = text("SELECT * FROM avaliacao") #LIMIT 100 OFFSET 100 para paginação
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambi pq cada linha é um objeto

        print(json)

        return json
    except Exception as e:
        return e


@avaliacao_bp.route('/update/<id>', methods=["PUT"])
def update(id):
    nota_final = request.form.get("nota_final")
    comentario = request.form.get("comentario")
    data_avaliacao = request.form.get("data_avaliacao")
    id_redacao = request.form.get("id_redacao")
    id_adm = request.form.get("id_adm")

    # Verifica se a avaliacao com o id existe
    exists_sql = text("SELECT 1 FROM avaliacao WHERE id = :id")
    exists = db.session.execute(exists_sql, {"id": id}).first()
    if not exists:
        return {"erro": f"Avaliacao com id {id} nao encontrado."}, 404

    if not nota_final or not nota_final.strip():
        return "Falta da nota explicita."
    if not comentario or not comentario.strip():
        return "Comentario inexistente. Informe dicas ao aluno."
    if not data_avaliacao or not data_avaliacao.strip():
        return "Falha ao procurar a data da avaliacao, digite logo a seguir."
    if not id_redacao or not id_redacao.strip():
        return "Diga qual a redacao que esta sendo avaliada."
    if not id_adm or not id_adm.strip():
       return "Avaliador não informado." 

    sql = text("UPDATE avaliacao SET nota_final = :nota_final, comentario = :comentario, data_avaliacao = :data_avaliacao, id_redacao = :id_redacao, id_adm = :id_adm WHERE id = :id") 
    dados = {"nota_final": nota_final, "comentario": comentario, "data_avaliacao": data_avaliacao, "id_redacao": id_redacao, "id_adm": id_adm, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Avaliacao com o id:{id} atualizado!"
    else:
        db.session.rollback()
        return f"problemas ao atualizar dados"

@avaliacao_bp.route('/delete/<id>', methods=["DELETE"])
def delete(id):
    sql = text("DELETE FROM avaliacao WHERE id = :id")
    dados = {"id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Avaliacao com o id:{id} removida"
    else:
        db.session.rollback()
        return f"Só deus na causa"

@avaliacao_bp.route("/dashboard/stats")
def status():
    #nota_final = request.form.get("nota_final")
    id_aluno = request.form.get("id_aluno")    

    #sql = text("SELECT AVG(nota_final) as media_geral, MAX(nota_final) as ultima_nota FROM avaliacao a JOIN redacoes r ON a.id_redacao = r.id JOIN usuario u ON r.id_aluno = u.id JOIN curso c ON u.numero_curso = c.id WHERE r.id_aluno = :id_aluno;")
    sql = text("SELECT AVG(nota_final) as media_geral, MAX(nota_final) as ultima_nota, u.numero_curso FROM avaliacao a JOIN redacoes r ON a.id_redacao = r.id JOIN usuario u ON r.id_aluno = u.id WHERE r.id_aluno = :id_aluno GROUP BY u.numero_curso;")
    dados_avaliacao = { "id_aluno": id_aluno}

    resultado = db.session.execute(sql, dados_avaliacao).mappings().first()
    
    if resultado is None:
        return {"erro": "Nenhuma avaliação encontrada para este aluno"}, 404
    
    numero_curso = resultado['numero_curso']
    media_geral = resultado['media_geral']
    ultima_nota = resultado['ultima_nota']

    sql_query = text("SELECT nota_corte FROM curso where id = :numero_curso")
    dados_curso = {"numero_curso": numero_curso}

    result = db.session.execute(sql_query, dados_curso).mappings().first()

    if result is None:
        return {"erro": "Nenhum curso encontrado."}

    if media_geral >= result['nota_corte']:
        return {"ultima_nota": ultima_nota, "media_geral": media_geral, "mensagem": "Aprovado para cursar!"}
    else:
        return {"ultima_nota": ultima_nota, "media_geral": media_geral, "mensagem": "Quase lá!"}
    
    