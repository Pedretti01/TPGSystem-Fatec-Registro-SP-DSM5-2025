from models.database import db, GamesQuestions

def get_all():
    return GamesQuestions.query.all()

def get_by_id(id):
    return GamesQuestions.query.get(id)

def create(idGameMatch, idQuestion, dateTime, pints):
    new = GamesQuestions(idGameMatch = idGameMatch,
                         idQuestion = idQuestion,
                         dateTime = dateTime,
                         pints = pints)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idGameMatch, idQuestion, dateTime, pints):
    rec = GamesQuestions.query.get(id)
    if rec:
        rec.idGameMatch = idGameMatch
        rec.idQuestion = idQuestion
        rec.dateTime = dateTime
        rec.pints = pints
        db.session.commit()
    return rec

def delete(id):
    rec = GamesQuestions.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
