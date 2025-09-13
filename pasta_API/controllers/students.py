from models.database import db, Students
from sqlalchemy import text

def authenticate(ra, password):
    rec = Students.query.filter_by(ra=ra, password=password).first()
    return rec

def get_all():
    sql = text("""
        SELECT s.id, s.name, s.ra, s.birth, s.idClass, y.descryption
        FROM Students s
        JOIN Classes c ON s.idClass = c.id
        JOIN YearsSeries y ON c.idYearSerie = y.id
    """)
    
    registers = db.session.execute(sql)
    
    students = []
    for rec in registers:
        students.append({
            'id': rec.id,
            'name': rec.name,
            'ra': rec.ra,
            'birth': rec.birth,
            'idClass': rec.idClass,
            'dsYearSerie': rec.descryption
        })
    
    return students
        
def get_by_id(id):
    sql = text("""
        SELECT s.id, s.name, s.ra, s.birth, s.idClass, y.descryption as dsYearSerie
        FROM Students s
        JOIN Classes c ON s.idClass = c.id
        JOIN YearsSeries y ON c.idYearSerie = y.id
        WHERE s.id = :id
    """)
    
    rec = db.session.execute(sql, {'id': id}).fetchone()

    if rec:
        return {
            'id': rec.id,
            'name': rec.name,
            'ra': rec.ra,
            'birth': rec.birth,
            'idClass': rec.idClass,
            'dsYearSerie': rec.descryption}
    return None

def create(name, ra, password, birth, idClass):
    new = Students(name = name,
                   ra = ra,
                   password = password,
                   birth = birth,
                   idClass = idClass)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, name, ra, password, birth, idClass):
    rec = Students.query.get(id)
    if rec:
        rec.name = name
        rec.ra = ra
        rec.password = password
        rec.birth = birth
        rec.idClass = idClass
        db.session.commit()
    return rec

def delete(id):
    rec = Students.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
