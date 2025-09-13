from models.database import db, Components

def get_all():
    return Components.query.all()

def get_by_id(id):
    return Components.query.get(id)
