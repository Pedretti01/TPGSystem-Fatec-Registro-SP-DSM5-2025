from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesQuestions import *
from sqlalchemy import text

gamesQuestions = Blueprint('gamesQuestions', __name__)

@gamesQuestions.route('/gamesQuestions', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 
                     'idGameMatch': rec.idGameMatch, 
                     'idQuestion': rec.idQuestion, 
                     'dateTime': rec.dateTime, 
                     'pints': rec.pints} for rec in all])

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id,  
                        'idGameMatch': rec.idGameMatch, 
                        'idQuestion': rec.idQuestion, 
                        'dateTime': rec.dateTime, 
                        'pints': rec.pints})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesQuestions.route('/gamesQuestions', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGameMatch' not in data:
        return jsonify({'error': 'Identificação da partida Inválido'}), 400
    if 'idQuestion' not in data:
        return jsonify({'error': 'validação Inválida'}), 400
    if 'dateTime' not in data:
        return jsonify({'error': 'Data Inválida'}), 400
    if 'pints' not in data:
        return jsonify({'error': 'Quantidade de pontos Inválida'}), 400

    rec = create(data['idGameMatch'], data['idQuestion'], data['dateTime'], data['pints'])

    return jsonify({'id': rec.id,  
                    'idGameMatch': rec.idGameMatch, 
                    'idQuestion': rec.idQuestion, 
                    'dateTime': rec.dateTime, 
                    'pints': rec.pints}), 201

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idGameMatch = data.get('idGameMatch')
    idQuestion = data.get('idQuestion')
    dateTime = data.get('dateTime')
    pints = data.get('pints')

    rec = update(id, idGameMatch, idQuestion, dateTime, pints)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idGameMatch': rec.idGameMatch, 
                        'idQuestion': rec.idQuestion, 
                        'dateTime': rec.dateTime, 
                        'pints': rec.pints})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['DELETE'])
def delete_(id):
    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
