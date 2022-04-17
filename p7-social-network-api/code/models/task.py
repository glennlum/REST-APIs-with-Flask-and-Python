import sqlite3
import datetime
from sqlalchemy import DateTime

from database import db


class TaskModel (db.Model):

    ''' 
    In a social networking system, users can post, like, 
    share, follow and unfollow. A TaskModel is a representation 
    of the the actions that users perform in the system. 
    '''

    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(50))    # actor's name
    verb = db.Column(db.String(50))     # an action to perform
    object = db.Column(db.String(50))   # a uniquely defined object reference
    target = db.Column(db.String(50))   # target's name
    datetime = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, actor, verb, object, target):
        '''
        Initialises a new task
        A task_id is only assigned when writing to cache
        '''
        self.task_id = None
        self.actor = actor
        self.verb = verb
        self.object = object
        self.target = target

    def json(self):
        '''
        Returns a json mapping of the task
        '''
        return {
            'actor': self.actor,
            'verb': self.verb,
            'object': self.object,
            'target': self.target
        }

    def json_with_id(self):
        '''
        Returns a json mapping of the task
        The id field is required when writing a task to cache
        '''
        return {
            'id': self.task_id,
            'actor': self.actor,
            'verb': self.verb,
            'object': self.object,
            'target': self.target
        }

    def set_id(self, _id):
        '''
        Assigns an id to the task obj
        '''
        self.task_id = _id

    def save_to_db(self):
        '''
        Inserts a row into the task table
        Returns the primary key value on insertion
        '''
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self.id

    @classmethod
    def find_by_object(cls, object):
        '''
        Finds the row containing the given object
        '''
        return cls.query.filter_by(object=object).first()

    @classmethod
    def find_by_actor(cls, actor):
        '''
        Finds all rows containing the given actor
        '''
        return cls.query.filter_by(actor=actor)

    @classmethod
    def is_shared_with_target(cls, actor, object, target):
        '''
        Finds the row where the actor shared the object with the target
        '''
        return cls.query.filter_by(actor=actor, verb='share', object=object, target=target).first()

    @classmethod
    def find_original_poster(cls, actor, object):
        '''
        Finds the row where the actor first posted the object
        '''
        return cls.query.filter_by(actor=actor, verb='post', object=object).first()

    @classmethod
    def is_liked_by_actor(cls, actor, object):
        '''
        Checks if an actor has liked a given object
        '''
        return cls.query.filter_by(actor=actor, verb='like', object=object).first()

    @classmethod
    def get_original_post_id(cls, object):
        '''
        Returns the id of the row where the object was originally posted
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tasks WHERE object=? AND verb=?"
        result = cursor.execute(query, (object, 'post'))
        row = result.fetchone()
        connection.close()
        if row:
            return row[0]

    @classmethod
    def insert_related(cls, task, related):
        '''
        Assigns an object to the related field of a task json mapping
        '''
        task['related'] = related
