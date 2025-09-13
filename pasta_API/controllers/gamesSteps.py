from models.database import db, GamesSteps

def get_all():
    return GamesSteps.query.all()

def get_by_id(id):
    return GamesSteps.query.get(id)

def create(idGameMatche, 
           idRegion, 
           dateTime, 
           completd):
    new = GamesSteps(idGameMatche = idGameMatche,
                     idRegion = idRegion,
                     dateTime = dateTime,
                     completd = completd)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, 
           idGameMatche, 
           idRegion, 
           dateTime, 
           completd):
    rec = GamesSteps.query.get(id)
    if rec:
        rec.idGameMatche = idGameMatche
        rec.idRegion = idRegion
        rec.dateTime = dateTime
        rec.completd = completd
        db.session.commit()
    return rec

def delete(id):
    rec = GamesSteps.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
