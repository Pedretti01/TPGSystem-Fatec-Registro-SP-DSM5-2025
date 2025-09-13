from models.database import db, Games
from sqlalchemy import text

def get_all():
    sql = text("""
        SELECT g.id, g.idStudent, s.name, g.idClasss, y.descryption, g.gold
        FROM Games g
        JOIN Students s ON g.idStudent = g.id
        JOIN Classes c ON g.idClass = c.id
        JOIN YearsSeries y ON c.idYearSerie = y.id
    """)
    
    registers = db.session.execute(sql)
    
    games = []
    for rec in registers:
        games.append({
            'id': rec.id, 
            'idStudent': rec.idStudent,
            'nmStudent': rec.name,
            'idClasss': rec.idClasss,
            'dsClass': rec.descryption,
            'gold': rec.gold
        })
    
    return games

def get_by_id(id):
    sql = text("""
        SELECT g.id, g.idStudent, s.name, g.idClasss, y.descryption, g.gold
        FROM Games g
        JOIN Students s ON g.idStudent = g.id
        JOIN Classes c ON g.idClass = c.id
        JOIN YearsSeries y ON c.idYearSerie = y.id
        WHERE g.id = :id
    """)
    
    rec = db.session.execute(sql, {'id': id}).fetchone()

    if rec:
        return {
            'id': rec.id, 
            'idStudent': rec.idStudent,
            'nmStudent': rec.name,
            'idClasss': rec.idClasss,
            'dsClass': rec.descryption,
            'gold': rec.gold}
    return None

def create(schoolYear, idYearSerie, idComponent, idTeacher):
    new = Games(schoolYear = schoolYear,
                idYearSerie = idYearSerie,
                idComponent = idComponent,
                idTeacher = idTeacher)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, schoolYear, idYearSerie, idComponent, idTeacher):
    rec = Games.query.get(id)
    if rec:
        rec.schoolYear = schoolYear
        rec.idYearSerie = idYearSerie
        rec.idComponent = idComponent
        rec.idTeacher = idTeacher
        db.session.commit()
    return rec

def delete(id):
    rec = Games.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
