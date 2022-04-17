from db import db


class UserModel (db.Model):

    '''Internal representation of a user'''

    # specify model for sqlalchemy
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # id automatically created by sqlalchemy
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # SELECT * FROM users WHERE username=username
        # returns user object model

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # returns user object model
