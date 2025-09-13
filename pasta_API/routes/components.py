from flask import Blueprint, request, jsonify
from controllers.components import *

components = Blueprint('components', __name__)

@components.route('/components', methods=['GET'])
def list():
    all = get_all()
    return jsonify([{'id': rec.id, 'descryption': rec.descryption} for rec in all])

@components.route('/components/<int:id>', methods=['GET'])
def get(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
