from flask import Blueprint, request, jsonify
from models.database import db
from controllers.questions import *
from sqlalchemy import text

questions = Blueprint('questions', __name__)

@questions.route('/questions', methods=['GET'])
def list_():
    return get_all()

@questions.route('/questions/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questions.route('/questions', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idQuestionType' not in data:
        return jsonify({'error': 'Tipo de Questão Inválido'}), 400
    if 'idRegion' not in data:
        return jsonify({'error': 'Região Inválida'}), 400
    if 'idTheme' not in data:
        return jsonify({'error': 'Tema Inválido'}), 400
    if 'question' not in data:
        return jsonify({'error': 'Questão Inválida'}), 400
    if 'idValidation1' not in data:
        return jsonify({'error': 'Validação 1 Inválida'}), 400
    if 'idValidation2' not in data:
        return jsonify({'error': 'Validação 2 Inválida'}), 400
    if 'idValidation3' not in data:
        return jsonify({'error': 'Validação 3 Inválida'}), 400
    if 'idValidation4' not in data:
        return jsonify({'error': 'Validação 4 Inválida'}), 400

    rec = create(data['idQuestionType'], 
                 data['idRegion'], 
                 data['idTheme'], 
                 data['question'], 
                 data['response1'], 
                 data['response2'], 
                 data['response3'], 
                 data['response4'], 
                 data['picture1'], 
                 data['picture2'], 
                 data['picture3'], 
                 data['picture4'], 
                 data['idValidation1'], 
                 data['idValidation2'], 
                 data['idValidation3'], 
                 data['idValidation4'])

    return jsonify({'id': rec.id,  
                    'idQuestionType': rec.idQuestionType,
                    'idRegion': rec.idRegion,
                    'idTheme': rec.idTheme,
                    'question': rec.question,
                    'response1': rec.response1,
                    'response2': rec.response2,
                    'response3': rec.response3,
                    'response4': rec.response4,
                    'picture1': rec.picture1,
                    'picture2': rec.picture2,
                    'picture3': rec.picture3,
                    'picture4': rec.picture4,
                    'idValidation1': rec.idValidation1,
                    'idValidation2': rec.idValidation2,
                    'idValidation3': rec.idValidation3,
                    'idValidation4': rec.idValidation4}), 201

@questions.route('/questions/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idQuestionType = data.get('idQuestionType') 
    idRegion = data.get('idRegion')
    idTheme = data.get('idTheme')
    question = data.get('question')
    response1 = data.get('response1')
    response2 = data.get('response2')
    response3 = data.get('response3')
    response4 = data.get('response4')
    picture1 = data.get('picture1')
    picture2 = data.get('picture2')
    picture3 = data.get('picture3')
    picture4 = data.get('picture4')
    idValidation1 = data.get('idValidationn1')
    idValidation2 = data.get('idValidation2')
    idValidation3 = data.get('idVaalidation3')
    idValidation4 = data.get('idValidation4')
           
    rec = update(id, 
                 idQuestionType, 
                 idRegion, 
                 idTheme, 
                 question, 
                 response1, 
                 response2, 
                 response3, 
                 response4, 
                 picture1, 
                 picture2, 
                 picture3, 
                 picture4, 
                 idValidation1, 
                 idValidation2, 
                 idValidation3, 
                 idValidation4)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idQuestionType': rec.idQuestionType,
                        'idRegion': rec.idRegion,
                        'idTheme': rec.idTheme,
                        'question': rec.question,
                        'response1': rec.response1,
                        'response2': rec.response2,
                        'response3': rec.response3,
                        'response4': rec.response4,
                        'picture1': rec.picture1,
                        'picture2': rec.picture2,
                        'picture3': rec.picture3,
                        'picture4': rec.picture4,
                        'idValidation1': rec.idValidation1,
                        'idValidation2': rec.idValidation2,
                        'idVaalidation3': rec.idValidation3,
                        'idValidation4': rec.idValidation4})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questions.route('/questions/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM QuestionsSkills WHERE idQuestion = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Questiões e Habilidades e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
