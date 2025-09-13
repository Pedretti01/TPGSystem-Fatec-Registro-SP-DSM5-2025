from flask import Blueprint, request, jsonify
from controllers.regions import *

regions = Blueprint('regions', __name__)

@regions.route('/regions', methods=['GET'])
def list():
    all = get_all()
    return jsonify([{'id': rec.id, 'descryption': rec.descryption} for rec in all])

@regions.route('/regions/<int:id>', methods=['GET'])
def get(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
