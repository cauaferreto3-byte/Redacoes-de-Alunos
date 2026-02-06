from flask import Flask
#import do banco de dados
from database import init_db

#Importar módulos 
from usuario import usuario_bp
from redacoes import redacoes_bp
from avaliacao import avaliacao_bp
from adm import adm_bp
from curso import curso_bp   
  
app = Flask(__name__)

#Conexao Geral do meu app
init_db(app)

#Registro de controladores 
app.register_blueprint(usuario_bp)
app.register_blueprint(redacoes_bp)
app.register_blueprint(avaliacao_bp)
app.register_blueprint(adm_bp)
app.register_blueprint(curso_bp)

if __name__ == "__main__":
    app.run(debug=True)