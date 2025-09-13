from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesMatches import *
from sqlalchemy import text

gamesMatches = Blueprint('gamesMatches', __name__)

@gamesMatches.route('/gamesMatches', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 
                     'idGame': rec.idGame,
                     'idCharacter': rec.idCharacter,
                     'name': rec.name,
                     'scorePoints': rec.scorePoints,
                     'scoreStrength': rec.scoreStrength,
                     'scoreAgility': rec.scoreAgility,
                     'scoreResistance': rec.scoreResistance,
                     'scoreWisdom': rec.scoreWisdom} for rec in all])

@gamesMatches.route('/gamesMatches/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id,  
                        'idGame': rec.idGame,
                        'idCharacter': rec.idCharacter,
                        'name': rec.name,
                        'scorePoints': rec.scorePoints,
                        'scoreStrength': rec.scoreStrength,
                        'scoreAgility': rec.scoreAgility,
                        'scoreResistance': rec.scoreResistance,
                        'scoreWisdom': rec.scoreWisdom})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesMatches.route('/gamesMatches', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGame' not in data:
        return jsonify({'error': 'Jogo Inválido'}), 400
    if 'idCharacter' not in data:
        return jsonify({'error': 'Personagem Inválido'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Nome Inválido'}), 400
    if 'scorePoints' not in data:
        return jsonify({'error': 'Pontos Inválidos'}), 400
    if 'scoreStrength' not in data:
        return jsonify({'error': 'Força Inválida'}), 400
    if 'scoreAgility' not in data:
        return jsonify({'error': 'Agilidade Inválida'}), 400
    if 'scoreResistance' not in data:
        return jsonify({'error': 'Resistência Inválida'}), 400
    if 'scoreWisdom' not in data:
        return jsonify({'error': 'Sabedoria Inválida'}), 400

    rec = create(data['idGame'], 
                 data['idCharacter'], 
                 data['name'], 
                 data['scorePoints'], 
                 data['scoreStrength'], 
                 data['scoreAgility'], 
                 data['scoreResistance'], 
                 data['scoreWisdom'])

    return jsonify({'id': rec.id,  
                    'idGame': rec.idGame,
                    'idCharacter': rec.idCharacter,
                    'name': rec.name,
                    'scorePoints': rec.scorePoints,
                    'scoreStrength': rec.scoreStrength,
                    'scoreAgility': rec.scoreAgility,
                    'scoreResistance': rec.scoreResistance,
                    'scoreWisdom': rec.scoreWisdom}), 201

@gamesMatches.route('/gamesMatches/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idGame = data.get('idGame') 
    idCharacter = data.get('idCharacter')
    name = data.get('name')
    scorePoints = data.get('scorePoints')
    scoreStrength = data.get('scoreStrength')
    scoreAgility = data.get('scoreAgility')
    scoreResistance = data.get('scoreResistance')
    scoreWisdom = data.get('scoreWisdom')
           
    rec = update(id, 
                 idGame, 
                 idCharacter, 
                 name, 
                 scorePoints, 
                 scoreStrength, 
                 scoreAgility, 
                 scoreResistance, 
                 scoreWisdom)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idGame': rec.idGame,
                        'idCharacter': rec.idCharacter,
                        'name': rec.name,
                        'scorePoints': rec.scorePoints,
                        'scoreStrength': rec.scoreStrength,
                        'scoreAgility': rec.scoreAgility,
                        'scoreResistance': rec.scoreResistance,
                        'scoreWisdom': rec.scoreWisdom})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesMatches.route('/gamesMatches/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM GamesQuestions WHERE idGameMatches = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Questiões da Partida e não pode ser excluído.'}), 400

    used = db.session.execute(
        text("SELECT COUNT(*) FROM GamesChallenges WHERE idGameMatches = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Desafions da Partida e não pode ser excluído.'}), 400

    used = db.session.execute(
        text("SELECT COUNT(*) FROM GamesSteps WHERE idGameMatches = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Passos da Partida e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
