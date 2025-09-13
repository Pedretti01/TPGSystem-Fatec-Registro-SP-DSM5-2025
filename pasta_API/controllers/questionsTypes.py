from models.database import db, QuestionsTypes

def get_all():
    return QuestionsTypes.query.all()

def get_by_id(id):
    return QuestionsTypes.query.get(id)
