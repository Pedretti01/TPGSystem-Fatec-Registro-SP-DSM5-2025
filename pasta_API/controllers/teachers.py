from models.database import db, Teachers

def authenticate(email, password):
    teacher = Teachers.query.filter_by(eMail=email, password=password).first()
    return teacher

def get_all():
    return Teachers.query.all()

def get_by_id(id):
    return Teachers.query.get(id)

def create(name, eMail, password):
    new = Teachers(name=name,
                   eMail=eMail,
                   password=password)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, name, eMail, password):
    rec = Teachers.query.get(id)
    if rec:
        rec.name = name
        rec.eMail = eMail
        rec.password = password
        db.session.commit()
    return rec

def delete(id):
    rec = Teachers.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
