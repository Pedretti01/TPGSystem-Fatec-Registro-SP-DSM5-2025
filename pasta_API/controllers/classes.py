from models.database import db, Classes

def get_all():
    registers = Classes.query.all()
    return [{'id': rec.id, 
            'schoolYear': rec.schoolYear,
            'idYearSerie': rec.idYearSerie,
            'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
            'idComponent': rec.idComponent,
            'dsComponent': rec.component.descryption if rec.component else None,
            'idTeacher': rec.idTeacher,
            'dsTeacher': rec.teacher.descryption if rec.teacher else None
            } for rec in registers]

def get_by_id(id):
    rec = Classes.query.get(id)
    return {'id': rec.id, 
            'schoolYear': rec.schoolYear,
            'idYearSerie': rec.idYearSerie,
            'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
            'idComponent': rec.idComponent,
            'dsComponent': rec.component.descryption if rec.component else None,
            'idTeacher': rec.idTeacher,
            'dsTeacher': rec.teacher.descryption if rec.teacher else None
            }

def create(schoolYear, idYearSerie, idComponent, idTeacher):
    new = Classes(schoolYear = schoolYear,
                  idYearSerie = idYearSerie,
                  idComponent = idComponent,
                  idTeacher = idTeacher)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, schoolYear, idYearSerie, idComponent, idTeacher):
    rec = Classes.query.get(id)
    if rec:
        rec.schoolYear = schoolYear
        rec.idYearSerie = idYearSerie
        rec.idComponent = idComponent
        rec.idTeacher = idTeacher
        db.session.commit()
    return rec

def delete(id):
    rec = Classes.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
