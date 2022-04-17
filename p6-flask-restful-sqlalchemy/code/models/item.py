from db import db


class ItemModel (db.Model):

    '''Internal representation of an item'''

    # specify model for sqlalchemy
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    # id automatically created by sqlalchemy
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # define foreign key
    store = db.relationship('StoreModel')
    # every 'item' model will have a store obj which matches its store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

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
