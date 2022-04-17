from db import db


class StoreModel (db.Model):

    '''Internal representation of a store'''

    # specify model for sqlalchemy
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    # id automatically created by sqlalchemy
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # every 'store' model will have a list of item objects
    # lazy='dynamic' does not go into the items table and create an obj of each item yet
    # only when requested

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
    # self.items is now a query builder that can retrieve the items when needed
    # will only look inside the items table when this method is called
    # trade off between speed of adding store to table and speed of calling json method

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # SELECT * FROM items WHERE name=name LIMIT 1
        # sqlalchemy returns an item model object

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # 'session' refers to a collection of objects that will be written to database in a batch
        #  method is used for both update and insert (upsert)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
