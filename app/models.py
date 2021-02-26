from app import db
from sqlalchemy.sql import func

from crypto import encrypt


class SecretMixin:
    @classmethod
    def create(cls, pwd, **kwargs):
        encrypted = encrypt(pwd)

        obj = cls(pwd=encrypted, **kwargs)

        db.session.add(obj)
        db.session.commit()
        
        return obj

    @classmethod
    def update_pwd(cls, id, pwd):
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__} object id: {self.id}, username: {self.username}, created at: {self.created}>'



class User(SecretMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))

    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    created = db.Column(db.DateTime, func.now())