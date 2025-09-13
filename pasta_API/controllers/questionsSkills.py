from models.database import db, QuestionsSkills

def get_all():
    registers = QuestionsSkills.query.all()
    return [{'id': rec.id, 
             'idQuestion': rec.idQuestion,
             'dsQuestion': rec.question.descryption if rec.question else None,
             'idSkill': rec.idSkill,
             'dsSkill': rec.skill.descryption if rec.skill else None,
             'idYearSerie': rec.idYearSerie,
             'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
             'difficult': rec.difficult,
             'available': rec.available} for rec in registers]

def get_by_id(id):
    rec = QuestionsSkills.query.get(id)
    if rec:
        return {'id': rec.id, 
                'idQuestion': rec.idQuestion,
                'dsQuestion': rec.question.descryption if rec.question else None,
                'idSkill': rec.idSkill,
                'dsSkill': rec.skill.descryption if rec.skill else None,
                'idYearSerie': rec.idYearSerie,
                'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
                'difficult': rec.difficult,
                'available': rec.available}
    return None

def create(idQuestion, idSkill, idYearSerie, difficult, available):
    new = QuestionsSkills(idQuestion = idQuestion,
                          idSkill = idSkill,
                          idYearSerie = idYearSerie,
                          difficult = difficult,
                          available = available)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idQuestion, idSkill, idYearSerie, difficult, available):
    rec = QuestionsSkills.query.get(id)
    if rec:
        rec.idQuestion = idQuestion
        rec.idSkill = idSkill
        rec.idYearSerie = idYearSerie
        rec.difficult = difficult
        rec.available = available
        db.session.commit()
    return rec

def delete(id):
    rec = QuestionsSkills.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
