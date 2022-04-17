from database import db


class RelatedModel (db.Model):

    '''
    A post may be related to multiple likes and shares.
    The RelatedModel links a post with an associated like
    and/or share.
    '''

    __tablename__ = 'related'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)     # a task id
    related_id = db.Column(db.Integer)  # a task id

    def __init__(self, task_id, related_id):
        '''
        Initialises a new 'related' record
        '''
        self.task_id = task_id
        self.related_id = related_id

    def save_to_db(self):
        '''
        Inserts row into the 'related' table
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes row from the 'related' table
        '''
        db.session.delete(self)
        db.session.commit()
