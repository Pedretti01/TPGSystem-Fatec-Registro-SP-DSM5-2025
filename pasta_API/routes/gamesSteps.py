from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesSteps import *
from sqlalchemy import text

gamesSteps = Blueprint('gamesSteps', __name__)

@gamesSteps.route('/gamesSteps', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 
                     'idGameMatch': rec.idGameMatch, 
                     'idRegion': rec.idRegion, 
                     'dateTime': rec.dateTime, 
                     'completd': rec.completd} for rec in all])

@gamesSteps.route('/gamesSteps/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id,  
                        'idGameMatch': rec.idGameMatch, 
                        'idRegion': rec.idRegion, 
                        'dateTime': rec.dateTime, 
                        'completd': rec.completd})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesSteps.route('/gamesSteps', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGameMatch' not in data:
        return jsonify({'error': 'Identificação da partida Inválido'}), 400
    if 'idRegion' not in data:
        return jsonify({'error': 'Região Inválida'}), 400
    if 'dateTime' not in data:
        return jsonify({'error': 'Data Inválida'}), 400
    if 'completd' not in data:
        return jsonify({'error': 'Indicação de Fase completa Inválida'}), 400

    rec = create(data['idGameMatch'], data['idRegion'], data['dateTime'], data['completd'])

    return jsonify({'id': rec.id,  
                    'idGameMatch': rec.idGameMatch, 
                    'idRegion': rec.idRegion, 
                    'dateTime': rec.dateTime, 
                    'completd': rec.completd}), 201

@gamesSteps.route('/gamesSteps/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idGameMatch = data.get('idGameMatch')
    idRegion = data.get('idRegion')
    dateTime = data.get('dateTime')
    completd = data.get('completd')

    rec = update(id, idGameMatch, idRegion, dateTime, completd)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idGameMatch': rec.idGameMatch, 
                        'idRegion': rec.idRegion, 
                        'dateTime': rec.dateTime, 
                        'completd': rec.pints})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesSteps.route('/gamesSteps/<int:id>', methods=['DELETE'])
def delete_(id):
    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
