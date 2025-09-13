from models.database import db, GamesChallenges

def get_all():
    return GamesChallenges.query.all()

def get_by_id(id):
    return GamesChallenges.query.get(id)

def create(idGameMatche, 
           number, 
           dateTime, 
           points):
    new = GamesChallenges(idGameMatche = idGameMatche,
                          number = number,
                          dateTime = dateTime,
                          points = points)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, 
           idGameMatche, 
           number, 
           dateTime, 
           points):
    rec = GamesChallenges.query.get(id)
    if rec:
        rec.idGameMatche = idGameMatche
        rec.number = number
        rec.dateTime = dateTime
        rec.points = points
        db.session.commit()
    return rec

def delete(id):
    rec = GamesChallenges.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
