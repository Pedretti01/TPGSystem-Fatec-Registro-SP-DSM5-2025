from flask import Blueprint, request, jsonify
from models.database import db
from controllers.students import *
from sqlalchemy import text
from werkzeug.security import generate_password_hash

students = Blueprint('students', __name__)

@students.route('/students/login', methods=['POST'])
def login_():
    data = request.get_json()
    
    ra = data.get('ra')
    password = data.get('password')

    if not ra or not password:
        return jsonify({'error': 'Ra e senha são obrigatórios'}), 400

    students = authenticate(ra, password)
    if students:
        return jsonify({
            'message': 'Login realizado com sucesso',
            'id': students.id,
            'name': students.name,
            'ra': students.ra
        }), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

@students.route('/students', methods=['GET'])
def list_():
    return get_all()

@students.route('/students/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@students.route('/students', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Nome Inválido'}), 400
    if 'ra' not in data:
        return jsonify({'error': 'RA Inválido'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Senha Inválida'}), 400
    if 'birth' not in data:
        return jsonify({'error': 'Aniversário Inválido'}), 400
    if 'idClass' not in data:
        return jsonify({'error': 'Classe Inválida'}), 400

    hashed_password = generate_password_hash(data['password']) 

    rec = create(data['name'], 
                 data['ra'], 
                 hashed_password, 
                 data['birth'], 
                 data['idClass'])

    return jsonify({'id': rec.id,  
                    'name': rec.name,
                    'ra': rec.ra,
                    'birth': rec.birth,
                    'idClass': rec.idClass}), 201

@students.route('/students/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    name = data.get('name')
    ra = data.get('ra')
    password = data.get('password')
    birth = data.get('birth')
    idClass = data.get('idClass')

    hashed_password = generate_password_hash(password) if password else None

    rec = update(id, name, ra, hashed_password, birth, idClass)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'name': rec.name,
                        'ra': rec.ra,
                        'birth': rec.birth,
                        'idClass': rec.idClass})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@students.route('/students/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Games WHERE idStudent = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na na tabela de Games e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
