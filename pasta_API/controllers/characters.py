from models.database import db, Characters

def get_all():
    registers = Characters.query.all()
    return [{'id': rec.id, 
             'number': rec.number, 
             'idValidation': rec.idValidation, 
             'dsValidation': rec.validation.descryption if rec.validation else None,
             'scoreStrength': rec.scoreStrength, 
             'scoreAgility': rec.scoreAgility, 
             'scoreResistance': rec.scoreResistance, 
             'scoreWisdom': rec.scoreWisdom} for rec in registers]

def get_by_id(id):
    rec = Characters.query.get(id)
    if rec:
        return {'id': rec.id, 
                'number': rec.number, 
                'idValidation': rec.idValidation, 
                'dsValidation': rec.validation.descryption if rec.validation else None,
                'scoreStrength': rec.scoreStrength, 
                'scoreAgility': rec.scoreAgility, 
                'scoreResistance': rec.scoreResistance, 
                'scoreWisdom': rec.scoreWisdom}
    return None
