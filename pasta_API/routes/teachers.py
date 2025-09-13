from flask import Blueprint, request, jsonify
from models.database import db
from controllers.teachers import *
from sqlalchemy import text
from werkzeug.security import generate_password_hash

teachers = Blueprint('teachers', __name__)

@teachers.route('/teachers/login', methods=['POST'])
def login_():
    data = request.get_json()
    
    email = data.get('eMail')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'E-mail e senha são obrigatórios'}), 400

    teacher = authenticate(email, password)
    if teacher:
        return jsonify({
            'message': 'Login realizado com sucesso',
            'id': teacher.id,
            'name': teacher.name,
            'email': teacher.eMail
        }), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

@teachers.route('/teachers', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 
                     'name': rec.name,
                     'eMail': rec.eMail} for rec in all])

@teachers.route('/teachers/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id,  
                        'name': rec.name,
                        'eMail': rec.eMail})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@teachers.route('/teachers', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Nome Inválido'}), 400
    if 'eMail' not in data:
        return jsonify({'error': 'e-Mail Inválido'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Senha Inválida'}), 400

    hashed_password = generate_password_hash(data['password'])

    rec = create(data['name'], data['eMail'], hashed_password)

    return jsonify({'id': rec.id,  
                    'name': rec.name,
                    'eMail': rec.eMail}), 201

@teachers.route('/teachers/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    name = data.get('name')
    eMail = data.get('eMail')
    password = data.get('password')

    hashed_password = generate_password_hash(password) if password else None

    rec = update(id, name, eMail, hashed_password)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'name': rec.name,
                        'eMail': rec.eMail})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@teachers.route('/teachers/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Classes WHERE idTeacher = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na Classe e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
