from flask import Blueprint, request, jsonify
from controllers.validations import *

validations = Blueprint('validations', __name__)

@validations.route('/validations', methods=['GET'])
def list():
    all = get_all()
    return jsonify([{'id': rec.id, 'descryption': rec.descryption} for rec in all])

@validations.route('/validations/<int:id>', methods=['GET'])
def get(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
