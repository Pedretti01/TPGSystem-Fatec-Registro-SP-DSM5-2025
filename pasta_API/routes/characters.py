from flask import Blueprint, request, jsonify
from controllers.characters import *

characters = Blueprint('characters', __name__)

@characters.route('/characters', methods=['GET'])
def list():
    return get_all()
    
@characters.route('/characters/<int:id>', methods=['GET'])
def get(id):
    rec = get_by_id(id)
    if rec:
        return rec
    return jsonify({'message': 'Registro Não Encontrado'}), 404
