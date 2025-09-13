from models.database import db, Validations

def get_all():
    return Validations.query.all()

def get_by_id(id):
    return Validations.query.get(id)
