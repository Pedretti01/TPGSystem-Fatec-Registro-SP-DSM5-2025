from models.database import db, Themes

def get_all():
    return Themes.query.all()

def get_by_id(id):
    return Themes.query.get(id)

def create(descryption):
    new = Themes(descryption=descryption)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, descryption):
    rec = Themes.query.get(id)
    if rec:
        rec.descryption = descryption
        rec.session.commit()
    return rec

def delete(id):
    rec = Themes.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
