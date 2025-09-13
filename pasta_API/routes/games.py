from flask import Blueprint, request, jsonify
from models.database import db
from controllers.games import *
from sqlalchemy import text

games = Blueprint('games', __name__)

@games.route('/games', methods=['GET'])
def list_():
    return get_all()

@games.route('/games/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@games.route('/games', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idStudent' not in data:
        return jsonify({'error': 'Estudante Inválido'}), 400
    if 'idClass' not in data:
        return jsonify({'error': 'Classe Inválida'}), 400

    rec = create(data['idStudent'], 
                 data['idClass'], 
                 data['gold'])

    return jsonify({'id': rec.id,  
                    'idStudent': rec.idStudent,
                    'idClass': rec.idClass,
                    'gold': rec.gold}), 201

@games.route('/games/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idStudent = data.get('idStudent')
    idClass = data.get('idClass')
    gold = data.get('gold')

    rec = update(id, idStudent, idClass, gold)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idStudent': rec.idStudent,
                        'idClass': rec.idClass,
                        'gold': rec.gold})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@games.route('/games/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM GamesMatches WHERE idGame = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na na tabela de Partidas e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
