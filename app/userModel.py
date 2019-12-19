import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from main import app, db

class UserModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullName = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime,default=datetime.datetime.utcnow)

    # CREATE User to DB
    def createUser(self):
        db.session.add(self)
        db.session.commit()
        return True

    @classmethod
    def findByEmail(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generateHash(password):
        return sha256.hash(password)

    @staticmethod
    def verifyHash(password, hash):
        return sha256.verify(password, hash)

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def isJtiBlacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)



