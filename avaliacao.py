from flask import Blueprint, request
from sqlalchemy import text
from database import db



avaliacao_bp = Blueprint('avaliacao', __name__, url_prefix = '/avaliacao') 

@avaliacao_bp.route('/create', methods=['POST'])
def inserirAvaliacao():
    #nota_final = request.form.get("nota_final")
    id_redacao = request.form.get("id_redacao")
    #comentario = request.form.get("comentario")
    #data_avaliacao = request.form.get("data_avaliacao")

    if not id_redacao:
        return "Informe a redação que está sendo avaliada!"

    sql = text("INSERT INTO avaliacao(nota_final, id_redacao, comentario, data_avaliacao) VALUES (:nota_final, :id_redacao, :comentario, :data_avaliacao)")
    dados = { #"nota_final": nota_final, 
        "id_redacao": id_redacao, 
         #"comentario": comentario, "data_avaliacao": data_avaliacao
         }

    db.session.execute(sql, dados)
    db.session.commit()

    return dados

@avaliacao_bp.route('/getOne/<id>')
def getOne(id):

    sql = text("SELECT * FROM avaliacao WHERE id = :id")
    dados = {"id": id}
    
    try:
        result = db.session.execute(sql, dados)
        #Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        
        return dict(linha)
    except Exception as e:
        return e




#getALL




@avaliacao_bp.route('/update/<id>', methods=["PUT"])
def update(id):
    nota_final = request.form.get("nota_final")
    comentario = request.form.get("comentario")
    data_avaliacao = request.form.get("data_avaliacao")

    sql = text("UPDATE avaliacao SET nota_final = :nota_final, comentario = :comentario, data_avaliacao = :data_avaliacao WHERE id = :id") 
    dados = {"nota_final": nota_final, "comentario": comentario, "data_avaliacao": data_avaliacao, "id": id}

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

#@avaliacao_bp.route("/essays/<id>/grade", methods=["PUT"])
#def corrigir_redacao(id):

 #   nota_final = request.form.get("nota_final")
  #  id_redacao = request.form.get("id_redacao")
   # comentario = request.form.get("comentario")

    #sql = text("UPDATE avaliacao SET nota_final = :nota_final, comentario = :comentario WHERE id = :id AND id_redacao = :id_redacao")
    #dados = {"id": id, "id_redacao": id_redacao, "nota_final": nota_final, "comentario": comentario}

    # result = db.session.execute(sql, dados)

    # linhas_afetadas = result.rowcount()

    #if linhas_afetadas == 1:
      #db.session.commit()
      #return "Sua redacao foi avaliada!"
    #else:
      #db.session.rollback()
      #return "Falha ao resgatar a redacao e/ou a avaliacao!"

    #copia e cola, mas depois tem que pensar melhor.