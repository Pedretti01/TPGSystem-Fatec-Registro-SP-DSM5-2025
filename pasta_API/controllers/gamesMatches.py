from models.database import db, GamesMatches

def get_all():
    return GamesMatches.query.all()

def get_by_id(id):
    return GamesMatches.query.get(id)

def create(idGame, 
           idCharacter, 
           name, 
           scorePoints, 
           scoreStrength, 
           scoreAgility, 
           scoreResistance, 
           scoreWisdom):
    new = GamesMatches(idGame = idGame,
                       idCharacter = idCharacter,
                       name = name,
                       scorePoints = scorePoints,
                       scoreStrength = scoreStrength,
                       scoreAgility = scoreAgility,
                       scoreResistance = scoreResistance,
                       scoreWisdom = scoreWisdom)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, 
           idGame, 
           idCharacter, 
           name, 
           scorePoints, 
           scoreStrength, 
           scoreAgility, 
           scoreResistance, 
           scoreWisdom):
    rec = GamesMatches.query.get(id)
    if rec:
        rec.idGame = idGame
        rec.idCharacter = idCharacter
        rec.name = name
        rec.scorePoints = scorePoints
        rec.scoreStrength = scoreStrength
        rec.scoreAgility = scoreAgility
        rec.scoreResistance = scoreResistance
        rec.scoreWisdom = scoreWisdom
        db.session.commit()
    return rec

def delete(id):
    rec = GamesMatches.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
