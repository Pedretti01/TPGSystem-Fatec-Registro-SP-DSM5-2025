from flask import Blueprint, request, jsonify
from models.database import db
from controllers.yearsSeries import *
from sqlalchemy import text

yearsSeries = Blueprint('yearsSeries', __name__)

@yearsSeries.route('/yearsSeries', methods=['GET'])
def list_():
    all = get_all()
    return jsonify([{'id': rec.id, 
                     'year': rec.year,
                     'serie': rec.serie,
                     'descryption': rec.descryption} for rec in all])

@yearsSeries.route('/yearsSeries/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({'id': rec.id,  
                        'year': rec.year,
                        'serie': rec.serie,
                        'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@yearsSeries.route('/yearsSeries', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'year' not in data:
        return jsonify({'error': 'Ano Inválido'}), 400
    if 'serie' not in data:
        return jsonify({'error': 'Série Inválida'}), 400
    if 'descryption' not in data:
        return jsonify({'error': 'Descrição Inválida'}), 400

    rec = create(data['year'], 
                 data['serie'], 
                 data['descryption'])

    return jsonify({'id': rec.id,  
                    'year': rec.year,
                    'serie': rec.serie,
                    'descryption': rec.descryption}), 201

@yearsSeries.route('/yearsSeries/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    year = data.get('year')
    serie = data.get('serie')
    descryption = data.get('descryption')

    rec = update(id, year, serie, descryption)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'year': rec.year,
                        'serie': rec.serie,
                        'descryption': rec.descryption})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@yearsSeries.route('/yearsSeries/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Classes WHERE idYearSerie = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na Classe e não pode ser excluído.'}), 400

    used = db.session.execute(
        text("SELECT COUNT(*) FROM questionsSkills WHERE idYearSerie = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado nas Habilidades por Questão e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
