from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Classe de Tipos de Questõess    
class QuestionsTypes(db.Model):
    __tablename__ = 'QuestionsTypes'
    id = db.Column(db.Integer, primary_key=True)
    descryption = db.Column(db.String(30), nullable=False)

    # Construtor
    def __init__(self, descryption):
        self.descryption = descryption

# Classe de Temas    
class Themes(db.Model):
    __tablename__ = 'Themes'
    id = db.Column(db.Integer, primary_key=True)
    descryption = db.Column(db.String(100), nullable=False)

    # Construtor
    def __init__(self, descryption):
        self.descryption = descryption

# # Classe de Regiões    
class Regions(db.Model):
    __tablename__ = 'Regions'
    id = db.Column(db.Integer, primary_key=True)
    descryption = db.Column(db.String(150), nullable=False)

    # Construtor
    def __init__(self, descryption):
        self.descryption = descryption

# Classe de Validações    
class Validations(db.Model):
    __tablename__ = 'Validations'
    id = db.Column(db.Integer, primary_key=True)
    descryption = db.Column(db.String(30), nullable=False)

    # Construtor
    def __init__(self, descryption):
        self.descryption = descryption

# Classe de Questões    
class Questions(db.Model):
    __tablename__ = 'Questions'
    id = db.Column(db.Integer, primary_key=True)
    idTheme = db.Column(db.Integer, db.ForeignKey('Themes.id'), nullable=False)
    idQuestionType = db.Column(db.Integer, db.ForeignKey('QuestionsTypes.id'), nullable=False)
    idRegion = db.Column(db.Integer, db.ForeignKey('Regions.id'))
    question = db.Column(db.String(500), nullable=False)
    response1 = db.Column(db.String(500))
    response2 = db.Column(db.String(500))
    response3 = db.Column(db.String(500))
    response4 = db.Column(db.String(500))
    picture1 = db.Column(db.LargeBinary)
    picture2 = db.Column(db.LargeBinary)
    picture3 = db.Column(db.LargeBinary)
    picture4 = db.Column(db.LargeBinary)
    idValidation1 = db.Column(db.Integer, db.ForeignKey('Validations.id'), nullable=False)
    idValidation2 = db.Column(db.Integer, db.ForeignKey('Validations.id'), nullable=False)
    idValidation3 = db.Column(db.Integer, db.ForeignKey('Validations.id'), nullable=False)
    idValidation4 = db.Column(db.Integer, db.ForeignKey('Validations.id'), nullable=False)

    theme = db.relationship('Themes', backref='Questions', lazy=True)
    questionType = db.relationship('QuestionsTypes', backref='Questions', lazy=True)
    region = db.relationship('Regions', backref='Questions', lazy=True)
    validation1 = db.relationship('Validations', foreign_keys=[idValidation1])
    validation2 = db.relationship('Validations', foreign_keys=[idValidation2])
    validation3 = db.relationship('Validations', foreign_keys=[idValidation3])
    validation4 = db.relationship('Validations', foreign_keys=[idValidation4])

    # Construtor
    def __init__(self, idQuestionType, idRegion, idTheme, question, response1, response2, response3, response4, picture1, picture2, picture3, picture4, idValidation1, idValidation2, idValidation3, idValidation4):
        self.idQuestionType = idQuestionType
        self.idRegion = idRegion
        self.idTheme = idTheme
        self.question = question
        self.response1 = response1
        self.response2 = response2
        self.response3 = response3
        self.response4 = response4
        self.picture1 = picture1
        self.picture2 = picture2
        self.picture3 = picture3
        self.picture4 = picture4
        self.idValidation1 = idValidation1
        self.idValidation2 = idValidation2
        self.idValidation3 = idValidation3
        self.idValidation4 = idValidation4
        
# Classe de Componantes   
class Components(db.Model):
    __tablename__ = 'Components'
    id = db.Column(db.Integer, primary_key=True)
    descryption = db.Column(db.String(50), nullable=False)

    # Construtor
    def __init__(self, descryption):
        self.descryption = descryption

# Classe de Habilidades   
class Skills(db.Model):
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    idComponent = db.Column(db.Integer, db.ForeignKey('Components.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500))
    skillCodeCP = db.Column(db.String(20))
    skillCodeBNCC = db.Column(db.String(20))

    component = db.relationship('Components', backref='Skills', lazy=True)

    # Construtor
    def __init__(self, idComponent, skill, comment, skillCodeCP, skillCodeBNCC):
        self.idComponent = idComponent
        self.skill = skill
        self.comment = comment
        self.skillCodeCP = skillCodeCP
        self.skillCodeBNCC = skillCodeBNCC
        
# Classe de AnosSeries   
class YearsSeries(db.Model):
    __tablename__ = 'YearsSeries'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    serie = db.Column(db.String(10), nullable=False)
    descryption = db.Column(db.String(50), nullable=False)

    # Construtor
    def __init__(self, year, serie, descryption):
        self.year = year
        self.serie = serie
        self.descryption = descryption

# Classe de Questões e Habilidades   
class QuestionsSkills(db.Model):
    __tablename__ = 'QuestionsSkills'
    id = db.Column(db.Integer, primary_key=True)
    idQuestion = db.Column(db.Integer, db.ForeignKey('Questions.id'), nullable=False)
    idSkill = db.Column(db.Integer, db.ForeignKey('Skills.id'), nullable=False)
    idYearSerie = db.Column(db.Integer, db.ForeignKey('YearsSeries.id'), nullable=False)
    difficulty = db.Column(db.Integer, default=1)
    available = db.Column(db.Boolean, default=False)

    question = db.relationship('Questions', backref='QuestionsSkills', lazy=True)
    skill = db.relationship('Skills', backref='QuestionsSkills', lazy=True)
    yearserie = db.relationship('YearsSeries', backref='QuestionsSkills', lazy=True)

    # Construtor
    def __init__(self, idQuestion, idSkill, idYearSerie, difficulty, available):
        self.idQuestion = idQuestion
        self.idSkill = idSkill
        self.idYearSerie = idYearSerie
        self.difficulty = difficulty
        self.available = available
        
# Classe de Professores   
class Teachers(db.Model):
    __tablename__ = 'Teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    eMail = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # Construtor
    def __init__(self, name, eMail, password):
        self.name = name
        self.eMail = eMail
        self.password = password
        
# Classe de Classes  
class Classes(db.Model):
    __tablename__ = 'Classes'
    id = db.Column(db.Integer, primary_key=True)
    schoolYear = db.Column(db.Integer, nullable=False)
    idYearSerie = db.Column(db.Integer, db.ForeignKey('YearsSeries.id'), nullable=False)
    idComponent = db.Column(db.Integer, db.ForeignKey('Components.id'), nullable=False)
    IdTeacher = db.Column(db.Integer, db.ForeignKey('Teachers.id'), nullable=False)

    yearSerie = db.relationship('YearsSeries', backref='Classes', lazy=True)
    component = db.relationship('Components', backref='Classes', lazy=True)
    teacher = db.relationship('Teachers', backref='Classes', lazy=True)

    # Construtor
    def __init__(self, schoolYear, idYearSerie, idComponent, IdTeacher):
        self.schoolYear = schoolYear
        self.idYearSerie = idYearSerie
        self.idComponent = idComponent
        self.IdTeacher = IdTeacher

# Classe de Estudantes   
class Students(db.Model):
    __tablename__ = 'Students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    ra = db.Column(db.String(20), nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    idClass = db.Column(db.Integer, db.ForeignKey('Classes.id'), nullable=False)

    classe = db.relationship('Classes', backref='Students', lazy=True)

    # Construtor
    def __init__(self, name, ra, password, birth, idClass):
        self.name = name
        self.ra = ra
        self.password = password
        self.birth = birth
        self.idClass = idClass

# Classe de Personagens   
class Characters(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    idValidation = db.Column(db.Integer, db.ForeignKey('Validations.id'), nullable=False)
    scoreStrength = db.Column(db.Integer, nullable=False, default=0)
    scoreAgility = db.Column(db.Integer, nullable=False, default=0)
    scoreResistance = db.Column(db.Integer, nullable=False, default=0)
    scoreWisdom = db.Column(db.Integer, nullable=False, default=0)

    validation = db.relationship('Validations', backref='characters', lazy=True)

    # Construtor
    def __init__(self, number, idValidation, scoreStrength, scoreAgility, scoreResistance, scoreWisdom):
        self.number = number
        self.idValidation = idValidation
        self.scoreStrength = scoreStrength
        self.scoreAgility = scoreAgility
        self.scoreResistance = scoreResistance
        self.scoreWisdom = scoreWisdom

# Classe de Jogos   
class Games(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    idStudent = db.Column(db.Integer, db.ForeignKey('Students.id'), nullable=False)
    idClass = db.Column(db.Integer, db.ForeignKey('Classes.id'), nullable=False)
    gold = db.Column(db.Integer, default=0)

    student = db.relationship('Students', backref='Games', lazy=True)
    classe = db.relationship('Classes', backref='Games', lazy=True)

    # Construtor
    def __init__(self, idStudent, idClass, gold):
        self.idStudent = idStudent
        self.idClass = idClass
        self.gold = gold

# Classe de JogosPartidas   
class GamesMatches(db.Model):
    __tablename__ = 'GamesMatches'
    id = db.Column(db.Integer, primary_key=True)
    idGame = db.Column(db.Integer, db.ForeignKey('Games.id'), nullable=False)
    idCharacter = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    scorePoints = db.Column(db.Integer, default=0)
    scoreStrength  = db.Column(db.Integer, default=0)
    scoreAgility = db.Column(db.Integer, default=0)
    scoreResistance = db.Column(db.Integer, default=0)
    scoreWisdom = db.Column(db.Integer, default=0)
    
    games = db.relationship('Games', backref='GamesMatches', lazy=True)
    character = db.relationship('Characters', backref='GamesMatches', lazy=True)

    # Construtor
    def __init__(self, idGame, idCharacter, name, scorePoints, scoreStrength, scoreAgility, scoreResistance, scoreWisdom):
        self.idGame = idGame
        self.idCharacter = idCharacter
        self.name = name
        self.scorePoints = scorePoints
        self.scoreStrength = scoreStrength
        self.scoreAgility = scoreAgility
        self.scoreResistance = scoreResistance
        self.scoreWisdom = scoreWisdom

# Classe de JogosQuestões   
class GamesQuestions(db.Model):
    __tablename__ = 'GamesQuestions'
    id = db.Column(db.Integer, primary_key=True)
    idGameMatch = db.Column(db.Integer, db.ForeignKey('GamesMatches.id'), nullable=False)
    idQuestion = db.Column(db.Integer, db.ForeignKey('Questions.id'), nullable=False)
    dateTime = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc), index=True)
    points = db.Column(db.Integer, default=0)
    
    gamematch = db.relationship('GamesMatches', backref='GamesQuestions', lazy=True)
    question = db.relationship('Questions', backref='GamesQuestions', lazy=True)

    # Construtor
    def __init__(self, idGameMatch, idQuestion, dateTime, points):
        self.idGameMatch = idGameMatch
        self.idQuestion = idQuestion
        self.dateTime = dateTime
        self.points = points

# Classe de JogosDesafios   
class GamesChallenges(db.Model):
    __tablename__ = 'GamesChallenges'
    id = db.Column(db.Integer, primary_key=True)
    idGameMatch = db.Column(db.Integer, db.ForeignKey('GamesMatches.id'), nullable=False)
    number = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc), index=True)
    points = db.Column(db.Integer, default=0)
    
    gamematch = db.relationship('GamesMatches', backref='GamesChallenges', lazy=True)

    # Construtor
    def __init__(self, idGameMatch, number, dateTime, points):
        self.idGameMatch = idGameMatch
        self.number = number
        self.dateTime = dateTime
        self.points = points

# Classe de JogosPassos   
class GamesSteps(db.Model):
    __tablename__ = 'GamesSteps'
    id = db.Column(db.Integer, primary_key=True)
    idGameMatch = db.Column(db.Integer, db.ForeignKey('GamesMatches.id'), nullable=False)
    idRegion = db.Column(db.Integer, db.ForeignKey('Regions.id'), nullable=False)
    dateTime = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc), index=True)
    completed = db.Column(db.Boolean, default=False)
    
    gamematch = db.relationship('GamesMatches', backref='GamesSteps', lazy=True)
    region = db.relationship('Regions', backref='GamesSteps', lazy=True)

    # Construtor
    def __init__(self, idGameMatch, idRegion, dateTime, completed):
        self.idGameMatch = idGameMatch
        self.idRegion = idRegion
        self.dateTime = dateTime
        self.completed = completed
