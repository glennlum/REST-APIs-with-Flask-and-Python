from database import db


class FollowModel (db.Model):

    '''
    A user can follow and be followed by other users.
    The FollowModel links a user with an associated follower.
    '''

    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String(50))     # follower's name
    followee = db.Column(db.String(50))     # followee's name

    def __init__(self, follower, followee):
        '''
        Initialises a new 'follow' record
        '''
        self.follower = follower
        self.followee = followee

    def get_follower(self):
        return self.follower

    def save_to_db(self):
        '''
        Inserts row into the 'follows' table
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes row from the 'follows' table
        '''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_row(cls, follower, followee):
        '''
        Find the row containing the given follower and followee
        '''
        return cls.query.filter_by(follower=follower, followee=followee).first()

    @classmethod
    def find_by_followee(cls, followee):
        '''
        Finds all rows related to a given followee
        '''
        return cls.query.filter_by(followee=followee)
