from flask import Flask, render_template
from routes.questionsTypes import questionsTypes
from routes.themes import themes
from routes.teachers import teachers
from routes.yearsSeries import yearsSeries
from routes.components import components
from routes.students import students
from routes.validations import validations
from routes.regions import regions
from routes.skills import skills
from routes.questions import questions
from routes.questionsSkills import questionsSkills
from routes.classes import classes
from routes.characters import characters
from routes.gamesQuestions import gamesQuestions
from routes.gamesMatches import gamesMatches
from routes.gamesChallenges import gamesChallenges
from routes.gamesSteps import gamesSteps

# Usar o banco MySQL
import pymysql

# Importar o modelo e banco de dados
from models.database import db

# Importar o CORS para permitir requisições de outros domínios
# from flask_cors import CORS

# Criando a instância do Flask
app = Flask(__name__)  

# Registra os blueprints de rotas
app.register_blueprint(questionsTypes)
app.register_blueprint(themes)
app.register_blueprint(teachers)
app.register_blueprint(yearsSeries)
app.register_blueprint(components)
app.register_blueprint(students)
app.register_blueprint(validations)
app.register_blueprint(regions)
app.register_blueprint(skills)
app.register_blueprint(questions)
app.register_blueprint(questionsSkills)
app.register_blueprint(classes)
app.register_blueprint(characters)
app.register_blueprint(gamesQuestions)
app.register_blueprint(gamesMatches)
app.register_blueprint(gamesChallenges)
app.register_blueprint(gamesSteps)

# Define o nome do banco de dados
DB_NAME = 'TPGSystem'
app.config['DATABASE_NAME'] = DB_NAME

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'tpgsystem'

# Permitir CORS
# CORS(app)  # Permite que o backend Flask aceite requisições de outros domínios

# Inicializa a aplicação e cria as tabelas do banco
if __name__ == '__main__':
    # Conecta ao MySQL para criar o banco de dados, se necessário
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',  
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Cria o banco de dados, se ele não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            # print(f"O banco de dados {DB_NAME} foi criado ou já existe!")
    except Exception as e:
        print(f"Erro ao criar banco de dados: {DB_NAME} - {str(e)}")
    finally:
        connection.close()

    # Inicializa o Flask e cria as tabelas do banco
    db.init_app(app=app)

    # Cria as tabelas antes da primeira requisição
    with app.app_context():
        db.create_all()        
        # print("Tabelas criadas com sucesso no banco de dados!")

    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
