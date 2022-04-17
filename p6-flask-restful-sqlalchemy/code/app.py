from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# during import sqlalchemy looks inside the class and creates the tables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# data.db file is located in root folder
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
# turn off flask sqlAlchemy modification tracker
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()
# Before the first request, this is going to create
# 'data.db' and relevant tables if it doesn't already exist


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
    # only assigns 'main' if python is running this file
    # if 'main' is not assigned, this file is only being imported
