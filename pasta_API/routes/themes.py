from flask import Blueprint, request, jsonify
from models.database import db
from controllers.themes import *
from sqlalchemy import text

themes = Blueprint('themes', __name__)

@themes.route('/themes', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 'descryption': rec.descryption} for rec in all])

@themes.route('/themes/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@themes.route('/themes', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'descryption' not in data:
        return jsonify({'error': 'Descrição Inválida'}), 400

    rec = create(data['descryption'])

    return jsonify({'id': rec.id, 'descryption': rec.descryption}), 201

@themes.route('/themes/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    rec = update(id, data.get('descryption'))
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@themes.route('/themes/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Questions WHERE idTheme = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este tema está sendo utilizado em questões e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
