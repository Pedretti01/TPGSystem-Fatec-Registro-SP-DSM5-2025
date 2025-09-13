from flask import Blueprint, request, jsonify
from models.database import db
from controllers.skills import *
from sqlalchemy import text

skills = Blueprint('skills', __name__)

@skills.route('/skills', methods=['GET'])
def list_():
    return get_all()

@skills.route('/skills/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return rec 
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@skills.route('/skills', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idComponent' not in data:
        return jsonify({'error': 'Componente Inválido'}), 400
    if 'skill' not in data:
        return jsonify({'error': 'Habilidade Inválida'}), 400

    rec = create(data['idComponent'], data['skill'], data['comment'], data['skillCodeCP'], data['SkillCodeBNCC'])

    return jsonify({'id': rec.id,  
                    'idComponent': rec.idComponent , 
                    'skill': rec.skill, 
                    'comment': rec.comment, 
                    'skillCodeCP': rec.skillCodeCP, 
                    'SkillCodeBNCC': rec.SkillCodeBNCC}), 201

@skills.route('/skills/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    idComponent = data.get('idComponent')
    skill = data.get('skill')
    comment = data.get('comment')
    skillCodeCP = data.get('skillCodeCP')
    SkillCodeBNCC = data.get('SkillCodeBNCC')

    rec = update(id, idComponent, skill, comment, skillCodeCP, SkillCodeBNCC)
    
    if rec:
        return jsonify({'id': rec.id,  
                        'idComponent': rec.idComponent , 
                        'skill': rec.skill, 
                        'comment': rec.comment, 
                        'skillCodeCP': rec.skillCodeCP, 
                        'SkillCodeBNCC': rec.SkillCodeBNCC})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@skills.route('/skills/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM QuestionsSkills WHERE idSkill = :id"), {'id': id}
    ).scalar()
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Questões por Habilidade e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
