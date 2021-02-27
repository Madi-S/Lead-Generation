from app import db
from sqlalchemy.sql import func

from crypto import encrypt


class SecretMixin:
    @classmethod
    def create(cls, pwd, **kwargs):
        encrypted = encrypt(pwd)

        obj = cls(password=encrypted, **kwargs)

        db.session.add(obj)
        db.session.commit()
        
        return obj

    @classmethod
    def validate_user(cls, username, pwd):
        obj = cls.query.filter_by(password=pwd).first()
        if obj and obj.password == encrypt(pwd):
            return True
        
    @classmethod
    def update_pwd(cls, id, pwd):
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} object id: {self.id}, username: {self.username}, created at: {self.created}>'



class User(SecretMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    created = db.Column(db.DateTime, default=func.now())
