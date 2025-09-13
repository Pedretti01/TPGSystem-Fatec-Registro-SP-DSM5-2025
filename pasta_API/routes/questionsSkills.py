from flask import Blueprint, request, jsonify
from models.database import db
from controllers.questionsSkills import *

questionsSkills = Blueprint('questionsSkills', __name__)

@questionsSkills.route('/questionsSkills', methods=['GET'])
def list_():
    return get_all()

@questionsSkills.route('/questionsSkills/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec 
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questionsSkills.route('/questionsSkills', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idQuestion' not in data:
        return jsonify({'error': 'Questão Inválida'}), 400
    if 'idSkill' not in data:
        return jsonify({'error': 'Habilidade Inválida'}), 400
    if 'idYearSerie' not in data:
        return jsonify({'error': 'Ano/Série Inválido'}), 400
    if 'difficult' not in data:
        return jsonify({'error': 'Dificuldade Inválida'}), 400
    if 'available' not in data:
        return jsonify({'error': 'Questão Liberada Inválida'}), 400

    rec = create(data['idQuestion'], data['idSkill'], data['idYearSerie'], data['difficult'], data['available'])

    return jsonify({'id': rec.id,  
                    'idQuestion': rec.idQuestion,
                    'idSkill': rec.idSkill,
                    'idYearSerie': rec.idYearSerie,
                    'difficult': rec.difficult,
                    'available': rec.available}), 201

@questionsSkills.route('/questionsSkills/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idQuestion = data.get('idQuestion') 
    idSkill = data.get('idSkill')
    idYearSerie = data.get('idYearSerie')
    difficult = data.get('difficult')
    available = data.get('available')
           
    rec = update(id, idQuestion, idSkill, idYearSerie, difficult, available)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idQuestion': rec.idQuestion,
                        'idSkill': rec.idSkill,
                        'idYearSerie': rec.idYearSerie,
                        'difficult': rec.difficult,
                        'available': rec.available})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questionsSkills.route('/questionsSkills/<int:id>', methods=['DELETE'])
def delete_(id):
    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
