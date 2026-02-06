from flask import Blueprint, request
from sqlalchemy import text
from database import db

curso_bp = Blueprint('curso', __name__, url_prefix = '/curso')

@curso_bp.route('/create', methods=['POST'])
def criar_curso():
    nome = request.form.get("nome")
    nota_corte = request.form.get("nota_corte")

    if not nome or not nome.strip():
        return {"erro": "Nome do curso não localizado."}, 400
    elif not nota_corte or not nota_corte.strip():
        return {"erro": "Nota inexistente, cheque se há algum valor inserido."}, 400
    elif nota_corte == 0:
        return {"erro": "Coloque uma nota maior que 0 para esse curso."}, 400
    
    sql = text("INSERT INTO curso (nome, nota_corte) VALUES (:nome, :nota_corte)")
    dados = {"nome": nome, "nota_corte": nota_corte}
    db.session.execute(sql, dados)
    db.session.commit()

    return dados
    

@curso_bp.route('/getOne/<id>')
def get_one_curso(id):

    sql = text("SELECT * FROM curso WHERE id = :id")
    dados = {"id": id}

    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e


@curso_bp.route('/getAll')
def get_all_curso():
    sql_query = text("SELECT * FROM curso") #LIMIT 100 OFFSET 100 para paginação
    
    try:
        #result sem dados
        result = db.session.execute(sql_query)
                
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] #Gambi pq cada linha é um objeto

        print(json)

        return json
    except Exception as e:
        return e

@curso_bp.route('/update/<id>', methods=["PUT"])
def updateCURSO(id):
    nome = request.form.get("nome")
    nota_corte = request.form.get("nota_corte")

    # Verifica se o administrador com o id existe
    exists_sql = text("SELECT 1 FROM curso WHERE id = :id")
    exists = db.session.execute(exists_sql, {"id": id}).first()
    if not exists:
        return {"erro": f"Curso com id {id} não encontrado."}, 404
    
    if not nome or not nome.strip():
        return {"erro": "Curso não encontrado."}, 400
    elif not nota_corte or not nota_corte.strip():
        return {"erro": "Campo nulo, digite o valor atual ou algo novo a esse curso."}, 400
    elif nota_corte == 0:
        return {"erro": "Coloque uma nota maior que 0 para esse curso."}, 400
    
    sql = text("UPDATE curso SET nome = :nome, nota_corte = :nota_corte WHERE id = :id") 
    dados = {"nome": nome, "nota_corte": nota_corte, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
   
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Curso com o id:{id} atualizado!"
    else:
        db.session.rollback()
        return f"problemas ao atualizar dados"
 
@curso_bp.route('/delete/<id>', methods=["DELETE"])
def delete_curso(id):
    sql = text("DELETE FROM curso WHERE id = :id")
    dados = {"id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount #conta quantas linhas foram afetadas
    
    if linhas_afetadas == 1: 
        db.session.commit()
        return f"Curso com o id:{id} removido"
    else:
        db.session.rollback()
        return f"Só deus na causa"