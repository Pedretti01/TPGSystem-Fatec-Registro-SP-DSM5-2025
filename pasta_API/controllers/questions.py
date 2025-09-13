from models.database import db, Questions

def get_all():
    registers = Questions.query.all()
    return [{'id': rec.id, 
             'idQuestionType': rec.idQuestionType,
             'dsQuestionType': rec.questionType.descryption if rec.questionType else None,
             'idRegion': rec.idRegion,
             'dsRegion': rec.region.descryption if rec.region else None,
             'idTheme': rec.idTheme,
             'dsThema': rec.theme.descryption if rec.theme else None,
             'question': rec.question,
             'response1': rec.response1,
             'response2': rec.response2,
             'response3': rec.response3,
             'response4': rec.response4,
#             'picture1': rec.picture1,
#             'picture2': rec.picture2,
#             'picture3': rec.picture3,
#             'picture4': rec.picture4,
             'idValidation1': rec.idValidation1,
             'dsValidation1': rec.validation1.descryption if rec.validation1 else None,
             'idValidation2': rec.idValidation2,
             'dsValidation2': rec.validation2.descryption if rec.validation2 else None,
             'idValidation3': rec.idValidation3,
             'dsValidation3': rec.validation3.descryption if rec.validation3 else None,
             'idValidation4': rec.idValidation4,
             'dsValidation4': rec.validation4.descryption if rec.validation4 else None
            } for rec in registers]

def get_by_id(id):
    rec = Questions.query.get(id)
    if rec:
        return {'id': rec.id, 
                'idQuestionType': rec.idQuestionType,
                'dsQuestionType': rec.questionType.descryption if rec.questionType else None,
                'idRegion': rec.idRegion,
                'dsRegion': rec.region.descryption if rec.region else None,
                'idTheme': rec.idTheme,
                'dsThema': rec.theme.descryption if rec.theme else None,
                'question': rec.question,
                'response1': rec.response1,
                'response2': rec.response2,
                'response3': rec.response3,
                'response4': rec.response4,
#                'picture1': rec.picture1,
#                'picture2': rec.picture2,
#                'picture3': rec.picture3,
#                'picture4': rec.picture4,
                'idValidation1': rec.idValidation1,
                'dsValidation1': rec.validation1.descryption if rec.validation1 else None,
                'idValidation2': rec.idValidation2,
                'dsValidation2': rec.validation2.descryption if rec.validation2 else None,
                'idValidation3': rec.idValidation3,
                'dsValidation3': rec.validation3.descryption if rec.validation3 else None,
                'idValidation4': rec.idValidation4,
                'dsValidation4': rec.validation4.descryption if rec.validation4 else None}
    return None

def create(idQuestionType, 
           idRegion, 
           idTheme, 
           question, 
           response1, 
           response2, 
           response3, 
           response4, 
           picture1, 
           picture2, 
           picture3, 
           picture4, 
           idVariation1, 
           idVariation2, 
           idVariation3, 
           idVariation4):
    new = Questions(idQuestionType = idQuestionType,
                    idRegion = idRegion,
                    idTheme = idTheme,
                    question = question,
                    response1 = response1,
                    response2 = response2,
                    response3 = response3,
                    response4 = response4,
                    picture1 = picture1,
                    picture2 = picture2,
                    picture3 = picture3,
                    picture4 = picture4,
                    idVariation1 = idVariation1,
                    idVariation2 = idVariation2,
                    idVariation3 = idVariation3,
                    idVariation4 = idVariation4)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, 
           idQuestionType, 
           idRegion, 
           idTheme, 
           question, 
           response1, 
           response2, 
           response3, 
           response4, 
           picture1, 
           picture2, 
           picture3, 
           picture4, 
           idVariation1, 
           idVariation2, 
           idVariation3, 
           idVariation4):
    rec = Questions.query.get(id)
    if rec:
        rec.idQuestionType = idQuestionType
        rec.idRegion = idRegion
        rec.idTheme = idTheme
        rec.question = question
        rec.response1 = response1
        rec.response2 = response2
        rec.response3 = response3
        rec.response4 = response4
        rec.picture1 = picture1
        rec.picture2 = picture2
        rec.picture3 = picture3
        rec.picture4 = picture4
        rec.idVariation1 = idVariation1
        rec.idVariation2 = idVariation2
        rec.idVariation3 = idVariation3
        rec.idVariation4 = idVariation4
        db.session.commit()
    return rec

def delete(id):
    rec = Questions.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
