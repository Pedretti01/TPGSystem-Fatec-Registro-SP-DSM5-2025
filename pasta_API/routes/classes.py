from flask import Blueprint, request, jsonify
from models.database import db
from controllers.classes import *
from sqlalchemy import text

classes = Blueprint('classes', __name__)

@classes.route('/classes', methods=['GET'])
def list_():
   return get_all()

@classes.route('/classes/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@classes.route('/classes', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'schoolYear' not in data:
        return jsonify({'error': 'Ano Letivo Inválido'}), 400
    if 'idYearSerie' not in data:
        return jsonify({'error': 'Ano/Série Inválido'}), 400
    if 'idComponent' not in data:
        return jsonify({'error': 'Componente Inválida'}), 400
    if 'idTeacher' not in data:
        return jsonify({'error': 'Professor Inválido'}), 400

    rec = create(data['schoolYear'], 
                 data['idYearSerie'], 
                 data['idComponent'], 
                 data['idTeacher'])

    return jsonify({'id': rec.id,  
                    'schoolYear': rec.schoolYear,
                    'idYearSerie': rec.ridYearSeriea,
                    'idComponent': rec.idComponent,
                    'idTeacher': rec.idTeacher}), 201

@classes.route('/classes/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    schoolYear = data.get('schoolYear')
    idYearSerie = data.get('idYearSerie')
    idComponent = data.get('idComponent')
    idTeacher = data.get('idTeacher')

    rec = update(id, schoolYear, idYearSerie, idComponent, idTeacher)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'schoolYear': rec.schoolYear,
                        'idYearSerie': rec.ridYearSeriea,
                        'idComponent': rec.idComponent,
                        'idTeacher': rec.idTeacher})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@classes.route('/classes/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Students WHERE idClasse = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado no Cadastro de Estudantes e não pode ser excluído.'}), 400

    used = db.session.execute(
        text("SELECT COUNT(*) FROM Games WHERE idClasse = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Games e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
