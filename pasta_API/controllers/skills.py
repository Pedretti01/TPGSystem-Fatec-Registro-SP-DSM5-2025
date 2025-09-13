from models.database import db, Skills

def get_all():
    registers =  Skills.query.all()
    return [{'id': rec.id, 
             'idComponent': rec.idComponent,
             'dsComponent': rec.component.descryption if rec.component else None,
             'skill': rec.skill,
             'comment': rec.comment,
             'skillCodeCP': rec.skillCodeCP,
             'SkillCodeBNCC': rec.SkillCodeBNCC} for rec in registers]

def get_by_id(id):
    rec = Skills.query.get(id)
    return {'id': rec.id, 
             'idComponent': rec.idComponent,
             'dsComponent': rec.component.descryption if rec.component else None,
             'skill': rec.skill,
             'comment': rec.comment,
             'skillCodeCP': rec.skillCodeCP,
             'SkillCodeBNCC': rec.SkillCodeBNCC}

def create(idComponent, skill, comment, skillCodeCP, SkillCodeBNCC):
    new = Skills(idComponent = idComponent,
                 skill = skill,
                 comment = comment,
                 skillCodeCP = skillCodeCP,
                 SkillCodeBNCC = SkillCodeBNCC)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idComponent, skill, comment, skillCodeCP, SkillCodeBNCC):
    rec = Skills.query.get(id)
    if rec:
        rec.idComponent = idComponent
        rec.skill = skill
        rec.comment = comment
        rec.skillCodeCP = skillCodeCP
        rec.SkillCodeBNCC = SkillCodeBNCC
        db.session.commit()
    return rec

def delete(id):
    rec = Skills.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
