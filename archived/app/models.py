from app import db
from sqlalchemy.sql import func

from crypto import encrypt


class ReprMixin:
    def __repr__(self):
        return f'<{self.__class__.__name__} object id: {self.id}, username: {self.username}, created at: {self.created}>'


class SecretMixin:
    @classmethod
    def create(cls, pwd, **kwargs):
        obj = cls(password=encrypt(pwd), **kwargs)

        db.session.add(obj)
        db.session.commit()

        print(f'Created: {obj}')

        return obj

    @classmethod
    def validate_user(cls, username, pwd):
        obj = cls.query.filter_by(username=username).first()
        print(f'User {username} found: {obj}')
        if obj and obj.password == encrypt(pwd):
            return obj

    @classmethod
    def update_pwd(cls, id, pwd):
        pass


class User(ReprMixin, SecretMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    created = db.Column(db.DateTime, default=func.now())
