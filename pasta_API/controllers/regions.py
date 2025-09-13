from models.database import db, Regions

def get_all():
    return Regions.query.all()

def get_by_id(id):
    return Regions.query.get(id)
