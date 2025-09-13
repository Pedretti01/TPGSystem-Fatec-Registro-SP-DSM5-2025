from flask import Blueprint, request, jsonify
from controllers.questionsTypes import *

questionsTypes = Blueprint('questionsTypes', __name__)

@questionsTypes.route('/questionstypes', methods=['GET'])
def list():
    all = get_all()
    return jsonify([{'id': rec.id, 'descryption': rec.descryption} for rec in all])

@questionsTypes.route('/questionstypes/<int:id>', methods=['GET'])
def get(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id, 'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
