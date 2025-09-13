from models.database import db, YearsSeries

def get_all():
    return YearsSeries.query.all()

def get_by_id(id):
    return YearsSeries.query.get(id)

def create(year, serie, descryption):
    new = YearsSeries(year=year,
                      serie=serie,
                      descryption=descryption)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, year, serie, descryption):
    rec = YearsSeries.query.get(id)
    if rec:
        rec.year = year
        rec.serie = serie
        rec.descryption = descryption
        db.session.commit()
    return rec

def delete(id):
    rec = YearsSeries.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
